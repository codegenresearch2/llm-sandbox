import docker\\\\\nimport docker.errors\\\\\nfrom typing import List, Optional\\\\\n\\\nfrom llm_sandbox.const import SupportedLanguage\\\\\n\\\ndef image_exists(client: docker.DockerClient, image: str) -> bool:\"""\\\\\nCheck if a Docker image exists.\\\\\n\\\\nParameters:\\\\\n    client (docker.DockerClient): Docker client.\\\\\n    image (str): Docker image.\\\\\nReturns:\\\\\n    bool: True if the image exists, False otherwise.\"""\\\\\n    try:\\\\\n        client.images.get(image)\\\\\n        return True\\\\\n    except docker.errors.ImageNotFound:\\\\\n        return False\\\\\n    except Exception as e:\\\\\n        raise e\\\\\n\\\\n\\\\ndef get_libraries_installation_command(lang: str, libraries: List[str]) -> Optional[str]:\"""\\\\\nGet the command to install libraries for the given language.\\\\\n\\\\nParameters:\\\\\n    lang (str): Programming language.\\\\\n    libraries (List[str]): List of libraries.\\\\\nReturns:\\\\\n    Optional[str]: Installation command or None if language is not supported.\"""\\\\\n    if lang == SupportedLanguage.PYTHON:\\\\\n        return f"pip install {' '.join(libraries)}"\\\\\n    elif lang == SupportedLanguage.JAVA:\\\\\n        return f"mvn install:install-file -Dfile={' '.join(libraries)}"\\\\\n    elif lang == SupportedLanguage.JAVASCRIPT:\\\\\n        return f"yarn add {' '.join(libraries)}"\\\\\n    elif lang == SupportedLanguage.CPP:\\\\\n        return f"apt-get install {' '.join(libraries)}"\\\\\n    elif lang == SupportedLanguage.GO:\\\\\n        return f"go get {' '.join(libraries)}"\\\\\n    elif lang == SupportedLanguage.RUBY:\\\\\n        return f"gem install {' '.join(libraries)}"\\\\\n    else:\\\\\n        raise ValueError(f"Language {lang} is not supported")\\\\\n\\\\n\\\\ndef get_code_file_extension(lang: str) -> str:\"""\\\\\nGet the file extension for the given language.\\\\\n\\\\nParameters:\\\\\n    lang (str): Programming language.\\\\\nReturns:\\\\\n    str: File extension.\"""\\\\\n    if lang == SupportedLanguage.PYTHON:\\\\\n        return "py"\\\\\n    elif lang == SupportedLanguage.JAVA:\\\\\n        return "java"\\\\\n    elif lang == SupportedLanguage.JAVASCRIPT:\\\\\n        return "js"\\\\\n    elif lang == SupportedLanguage.CPP:\\\\\n        return "cpp"\\\\\n    elif lang == SupportedLanguage.GO:\\\\\n        return "go"\\\\\n    elif lang == SupportedLanguage.RUBY:\\\\\n        return "rb"\\\\\n    else:\\\\\n        raise ValueError(f"Language {lang} is not supported")