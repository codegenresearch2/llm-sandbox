import io
import os
import docker
import tarfile
from typing import List, Optional, Union

from docker.models.images import Image
from docker.models.containers import Container
from llm_sandbox.utils import (
    image_exists,
    get_libraries_installation_command,
    get_code_file_extension,
    get_code_execution_command,
)
from llm_sandbox.const import SupportedLanguage, SupportedLanguageValues, DefaultImage, NotSupportedLibraryInstallation

class SandboxSession:
    """
    A class used to create a sandbox session for executing code in a Docker container.

    ...

    Attributes
    ----------
    lang : str
        the language of the code
    client : docker.DockerClient
        the Docker client
    image : Union[Image, str]
        the Docker image to use
    dockerfile : Optional[str]
        the path to the Dockerfile, if image is not provided
    container : Optional[Container]
        the Docker container
    path : Optional[str]
        the path to the Dockerfile
    keep_template : bool
        if True, the image and container will not be removed after the session ends
    is_create_template : bool
        if True, the image was created during this session
    verbose : bool
        if True, print messages

    Methods
    -------
    open():
        Open the Docker container.
    close():
        Close the Docker container.
    run(code: str, libraries: Optional[List] = None):
        Run the provided code in the Docker container.
    copy_from_runtime(src: str, dest: str):
        Copy a file from the Docker container to the host machine.
    copy_to_runtime(src: str, dest: str):
        Copy a file from the host machine to the Docker container.
    execute_command(command: Optional[str]):
        Execute a command in the Docker container.
    """

    def __init__(
        self,
        image: Optional[str] = None,
        dockerfile: Optional[str] = None,
        lang: str = SupportedLanguage.PYTHON,
        keep_template: bool = False,
        verbose: bool = True,
    ):
        # Initialization code...

    def open(self):
        # Open the Docker container code...

    def close(self):
        # Close the Docker container code...

    def run(self, code: str, libraries: Optional[List] = None):
        if not self.container:
            raise RuntimeError(
                "Session is not open. Please call open() method before running code."
            )

        if libraries:
            if self.lang.upper() in NotSupportedLibraryInstallation:
                raise ValueError(
                    f"Library installation has not been supported for {self.lang} yet!"
                )

            command = get_libraries_installation_command(self.lang, libraries)
            self.execute_command(command)

        code_file = f"/tmp/code.{get_code_file_extension(self.lang)}"
        with open(code_file, "w") as f:
            f.write(code)

        self.copy_to_runtime(code_file, code_file)
        output = self.execute_command(get_code_execution_command(self.lang, code_file))
        return output

    def copy_from_runtime(self, src: str, dest: str):
        # Copy a file from the Docker container to the host machine code...

    def copy_to_runtime(self, src: str, dest: str):
        # Copy a file from the host machine to the Docker container code...

    def execute_command(self, command: Optional[str]):
        # Execute a command in the Docker container code...

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()