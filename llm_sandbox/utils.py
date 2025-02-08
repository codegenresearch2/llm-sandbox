import docker\\\\\\nfrom typing import List, Optional\\\\\\\n\\\\\\\nclass SupportedLanguage:\\\\\\n    PYTHON = 'python'\\\\\\\\n    JAVA = 'java'\\\\\\\\n    JAVASCRIPT = 'javascript'\\\\\\\\n    CPP = 'cpp'\\\\\\\\n    GO = 'go'\\\\\\\\n    RUBY = 'ruby'\\\\\\\\n\\\\\\\ndef check_image_exists(client, image) -> bool:\\\\\\n    try:\\\\\\n        client.images.get(image)\\\\\\n        return True\\\\\\\\n    except docker.errors.ImageNotFound:\\\\\\n        return False\\\\\\\\n    except Exception as e:\\\\\\n        raise e\\\\\\\\n\\\\\\\ndef get_libraries_installation_command(lang, libraries) -> Optional[str]:\\\\\\\\n    if lang == SupportedLanguage.PYTHON:\\\\\\n        return f'pip install {' '.join(libraries)}'\\\\\\\\n    elif lang == SupportedLanguage.JAVA:\\\\\\n        return f'mvn install:install-file -Dfile={' '.join(libraries)}'\\\\\\\\n    elif lang == SupportedLanguage.JAVASCRIPT:\\\\\\n        return f'yarn add {' '.join(libraries)}'\\\\\\\\n    elif lang == SupportedLanguage.CPP:\\\\\\n        return f'apt-get install {' '.join(libraries)}'\\\\\\\\n    elif lang == SupportedLanguage.GO:\\\\\\n        return f'go get {' '.join(libraries)}'\\\\\\\\n    elif lang == SupportedLanguage.RUBY:\\\\\\n        return f'gem install {' '.join(libraries)}'\\\\\\\\n    else:\\\\\\n        raise ValueError(f'Language {lang} is not supported')'\\\\\\\\n\\\\\\\ndef get_code_file_extension(lang) -> str:\\\\\\n    if lang == SupportedLanguage.PYTHON:\\\\\\n        return 'py'\\\\\\\\n    elif lang == SupportedLanguage.JAVA:\\\\\\n        return 'java'\\\\\\\\n    elif lang == SupportedLanguage.JAVASCRIPT:\\\\\\n        return 'js'\\\\\\\\n    elif lang == SupportedLanguage.CPP:\\\\\\n        return 'cpp'\\\\\\\\n    elif lang == SupportedLanguage.GO:\\\\\\n        return 'go'\\\\\\\\n    elif lang == SupportedLanguage.RUBY:\\\\\\n        return 'rb'\\\\\\\\n    else:\\\\\\n        raise ValueError(f'Language {lang} is not supported')'\\\\\\\\n