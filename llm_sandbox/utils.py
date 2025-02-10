import docker
import docker.errors
from typing import List, Optional

from docker import DockerClient
from llm_sandbox.const import SupportedLanguage, NotSupportedLibraryInstallation, SupportedLanguageValues


def image_exists(client: DockerClient, image: str) -> bool:
    """
    Check if a Docker image exists
    :param client: Docker client
    :param image: Docker image
    :return: True if the image exists, False otherwise
    """
    try:
        client.images.get(image)
        return True
    except docker.errors.ImageNotFound:
        return False
    except Exception as e:
        raise e


def get_libraries_installation_command(lang: str, libraries: List[str]) -> Optional[str]:
    """
    Get the command to install libraries for the given language
    :param lang: Programming language
    :param libraries: List of libraries
    :return: Installation command or None if the language is not supported
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
    else:
        raise ValueError(f"Language {lang} is not supported")


def get_code_file_extension(lang: str) -> str:
    """
    Get the file extension for the given language
    :param lang: Programming language
    :return: File extension
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


def get_code_execution_command(lang: str, code_file: str) -> str:
    """
    Get the command to execute the code
    :param lang: Programming language
    :param code_file: Path to the code file
    :return: Execution command
    """
    if lang == SupportedLanguage.PYTHON:
        return f"python {code_file}"
    elif lang == SupportedLanguage.JAVA:
        return f"java {code_file}"
    elif lang == SupportedLanguage.JAVASCRIPT:
        return f"node {code_file}"
    elif lang == SupportedLanguage.CPP:
        return f"./{code_file}"
    elif lang == SupportedLanguage.GO:
        return f"go run {code_file}"
    elif lang == SupportedLanguage.RUBY:
        return f"ruby {code_file}"
    else:
        raise ValueError(f"Language {lang} is not supported")


def run_code_in_loop(lang: str, code: str, libraries: List[str] = None):
    """
    Run code in a loop with consistent handling of multiple execution commands
    :param lang: Programming language
    :param code: Code to run
    :param libraries: List of libraries to install
    """
    if libraries is None:
        libraries = []

    code_file_extension = get_code_file_extension(lang)
    with open(f"temp_code.{code_file_extension}", "w") as f:
        f.write(code)

    execution_command = get_code_execution_command(lang, f"temp_code.{code_file_extension}")
    if get_libraries_installation_command(lang, libraries) is not None:
        install_command = get_libraries_installation_command(lang, libraries)
        print(f"Installing libraries: {install_command}")

    print(f"Executing command: {execution_command}")
    # Execute the command


def test_directory_existence(directory_path: str):
    """
    Test command to verify directory existence
    :param directory_path: Path to the directory
    """
    import os
    if os.path.exists(directory_path):
        print(f"Directory {directory_path} exists.")
    else:
        print(f"Directory {directory_path} does not exist.")


# Example usage
if __name__ == "__main__":
    python_code = """
    print('Hello, World!')
    import numpy as np
    print(np.random.rand())
    """
    run_code_in_loop(SupportedLanguage.PYTHON, python_code, libraries=["numpy"])

    java_code = """
    public class Main {
        public static void main(String[] args) {
            System.out.println("Hello, World!");
        }
    }
    """
    run_code_in_loop(SupportedLanguage.JAVA, java_code)

    javascript_code = """
    console.log('Hello, World!');
    const axios = require('axios');
    axios.get('https://jsonplaceholder.typicode.com/posts/1')
        .then(response => console.log(response.data));
    """
    run_code_in_loop(SupportedLanguage.JAVASCRIPT, javascript_code, libraries=["axios"])

    cpp_code = """
    #include <iostream>
    int main() {
        std::cout << "Hello, World!" << std::endl;
        return 0;
    }
    """
    run_code_in_loop(SupportedLanguage.CPP, cpp_code)