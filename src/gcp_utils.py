import os
from pathlib import Path

from google.cloud.storage import Client, transfer_manager

from config import setup_logging


def upload_directory_with_transfer_manager(bucket_name, source_directory, workers=8):
    """Upload every file in a directory, including all files in subdirectories.

    Each blob name is derived from the filename, not including the `directory`
    parameter itself. For complete control of the blob name for each file (and
    other aspects of individual blob metadata), use
    transfer_manager.upload_many() instead.
    """

    logger = setup_logging(os.path.basename(__file__).split(".")[0])

    storage_client = Client()
    bucket = storage_client.bucket(bucket_name)

    ## Generate a list of paths (in string form) relative to the `directory`.

    # First, recursively get all files in `directory` as Path objects.
    directory_as_path_obj = Path(source_directory)
    paths = directory_as_path_obj.rglob("*")

    # Filter so the list only includes files, not directories themselves.
    file_paths = [path for path in paths if path.is_file()]

    # These paths are relative to the current working directory. Next, make them
    # relative to `directory`
    relative_paths = [path.relative_to(source_directory) for path in file_paths]

    # Finally, convert them all to strings.
    string_paths = [str(path) for path in relative_paths]

    logger.info("Found {} files.".format(len(string_paths)))

    # Start the upload.
    results = transfer_manager.upload_many_from_filenames(
        bucket,
        string_paths,
        upload_kwargs={"timeout": 600},
        source_directory=source_directory,
        max_workers=workers,
    )

    for name, result in zip(string_paths, results):
        # The results list is either `None` or an exception for each filename in
        # the input list, in order.

        if isinstance(result, Exception):
            logger.error(
                "Failed to upload {} due to exception: {}".format(name, result)
            )
        else:
            logger.info("Uploaded {} to {}.".format(name, bucket.name))
