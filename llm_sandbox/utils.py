import docker
import docker.errors
from typing import List, Optional

from docker import DockerClient
from llm_sandbox.const import SupportedLanguage, DefaultImage, NotSupportedLibraryInstallation, SupportedLanguageValues

def image_exists(client: DockerClient, image: str) -> bool:
    """
    Check if a Docker image exists.

    Parameters:
    client (DockerClient): Docker client.
    image (str): Docker image.

    Returns:
    bool: True if the image exists, False otherwise.
    """
    try:
        client.images.get(image)
        return True
    except docker.errors.ImageNotFound:
        return False

def get_libraries_installation_command(lang: str, libraries: List[str]) -> Optional[str]:
    """
    Get the command to install libraries for the given language.

    Parameters:
    lang (str): Programming language.
    libraries (List[str]): List of libraries.

    Returns:
    Optional[str]: Installation command.

    Raises:
    ValueError: If the language is not supported.
    """
    if lang == SupportedLanguage.PYTHON:
        return f"pip install {' '.join(libraries)}"
    elif lang == SupportedLanguage.JAVA:
        return f"mvn install:install-file -Dfile={' '.join(libraries)}"
    elif lang == SupportedLanguage.JAVASCRIPT:
        return f"yarn add {' '.join(libraries)}"
    elif lang == SupportedLanguage.CPP:
        return f"apt-get install {' '.join(libraries)}"
    elif lang == SupportedLanguage.GO:
        return f"go get {' '.join(libraries)}"
    elif lang == SupportedLanguage.RUBY:
        return f"gem install {' '.join(libraries)}"

    raise ValueError(f"Language {lang} is not supported")

def get_code_file_extension(lang: str) -> str:
    """
    Get the file extension for the given language.

    Parameters:
    lang (str): Programming language.

    Returns:
    str: File extension.

    Raises:
    ValueError: If the language is not supported.
    """
    if lang == SupportedLanguage.PYTHON:
        return "py"
    elif lang == SupportedLanguage.JAVA:
        return "java"
    elif lang == SupportedLanguage.JAVASCRIPT:
        return "js"
    elif lang == SupportedLanguage.CPP:
        return "cpp"
    elif lang == SupportedLanguage.GO:
        return "go"
    elif lang == SupportedLanguage.RUBY:
        return "rb"
    else:
        raise ValueError(f"Language {lang} is not supported")

def get_code_execution_command(lang: str, code_file: str) -> List[str]:
    """
    Get the command to execute the code.

    Parameters:
    lang (str): Programming language.
    code_file (str): Path to the code file.

    Returns:
    List[str]: Execution commands.

    Raises:
    ValueError: If the language is not supported.
    """
    if lang == SupportedLanguage.PYTHON:
        return [f"python {code_file}"]
    elif lang == SupportedLanguage.JAVA:
        return [f"java {code_file.split('.')[0]}"]
    elif lang == SupportedLanguage.JAVASCRIPT:
        return [f"node {code_file}"]
    elif lang == SupportedLanguage.CPP:
        return [f"g++ -o a.out {code_file}", f"./a.out"]
    elif lang == SupportedLanguage.GO:
        return [f"go run {code_file}"]
    elif lang == SupportedLanguage.RUBY:
        return [f"ruby {code_file}"]
    else:
        raise ValueError(f"Language {lang} is not supported")

def test_directory_existence(directory: str) -> bool:
    """
    Test if a directory exists.

    Parameters:
    directory (str): Directory path.

    Returns:
    bool: True if the directory exists, False otherwise.
    """
    import os
    return os.path.isdir(directory)

def run_code(lang: str, code: str, libraries: List[str] = None, test_directory: str = None):
    """
    Run the code with the given language and libraries.

    Parameters:
    lang (str): Programming language.
    code (str): Code to be executed.
    libraries (List[str], optional): List of libraries to be installed. Defaults to None.
    test_directory (str, optional): Directory to be tested for existence. Defaults to None.

    Returns:
    str: Output of the code execution.

    Raises:
    ValueError: If the test directory does not exist.
    """
    if libraries is None:
        libraries = []

    if test_directory and not test_directory_existence(test_directory):
        raise ValueError(f"Directory {test_directory} does not exist")

    client = docker.from_env()
    image = getattr(DefaultImage, lang.upper())

    if not image_exists(client, image):
        client.images.pull(image)

    container = client.containers.run(image, detach=True, tty=True)

    code_file = f"code.{get_code_file_extension(lang)}"
    container.put_archive("/app", code.encode())

    if libraries:
        install_command = get_libraries_installation_command(lang, libraries)
        container.exec_run(install_command, workdir="/app")

    exec_commands = get_code_execution_command(lang, code_file)
    output = ""
    for command in exec_commands:
        exit_code, command_output = container.exec_run(command, workdir="/app")
        output += command_output.decode()

    container.stop()
    container.remove()

    return output