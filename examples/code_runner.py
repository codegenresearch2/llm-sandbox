from llm_sandbox import SandboxSession

def run_code(lang: str, code: str, libraries: list = None):
    with SandboxSession(lang=lang, keep_template=True, verbose=True) as session:
        if libraries:
            session.execute_command(f"pip install {' '.join(libraries)}")

        output = session.run(code, libraries=libraries)
        print(output)

def run_python_code():
    run_code(
        lang="python",
        code="print('Hello, World!')"
    )

    run_code(
        lang="python",
        code="""
import numpy as np
print(np.random.rand())
""",
        libraries=["numpy"]
    )

    run_code(
        lang="python",
        code="""
import pandas as pd
print(pd.__version__)
""",
        libraries=["pandas"]
    )

def run_java_code():
    run_code(
        lang="java",
        code="""
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
"""
    )

def run_javascript_code():
    run_code(
        lang="javascript",
        code="console.log('Hello, World!')"
    )

    run_code(
        lang="javascript",
        code="""
const axios = require('axios');
axios.get('https://jsonplaceholder.typicode.com/posts/1')
    .then(response => console.log(response.data));
""",
        libraries=["axios"]
    )

def run_cpp_code():
    run_code(
        lang="cpp",
        code="""
#include <iostream>
int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
"""
    )

    run_code(
        lang="cpp",
        code="""
#include <iostream>
#include <vector>
int main() {
    std::vector<int> v = {1, 2, 3, 4, 5};
    for (int i : v) {
        std::cout << i << " ";
    }
    std::cout << std::endl;
    return 0;
}
"""
    )

    run_code(
        lang="cpp",
        code="""
#include <iostream>
#include <vector>
#include <algorithm>
int main() {
    std::vector<int> v = {1, 2, 3, 4, 5};
    std::reverse(v.begin(), v.end());
    for (int i : v) {
        std::cout << i << " ";
    }
    std::cout << std::endl;
    return 0;
}
""",
        libraries=["libstdc++"]
    )

if __name__ == "__main__":
    run_python_code()
    run_java_code()
    run_javascript_code()
    run_cpp_code()