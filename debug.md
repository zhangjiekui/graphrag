pip install poethepoet
poetry self add 'poethepoet[poetry_plugin]'

调试自己的文件：
点击顶部菜单：运行 -> 添加配置 -> Python 调试程序，当前文件

禁用ruff警告：
修改D:\pyprojects\graphrag\pyproject.toml
以# 注释掉ruff相关的配置项目
如：
[tool.poe.tasks]
#_sort_imports = "ruff check --select I --fix ."
#_format_code = "ruff format  ."
#_ruff_check = 'ruff check .'

#check_format = 'ruff format . --check'
#fix = "ruff check --fix ."
#fix_unsafe = "ruff check --fix --unsafe-fixes ."

在[tool.ruff]节添加一句line-length = 120
target-version = "py310"
extend-include = ["*.ipynb"]
line-length = 120

