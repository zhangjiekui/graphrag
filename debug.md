创建虚拟环境
CTRL + SHIPT + P
> Python:创建虚拟环境
  Venv 在当前工作区中创建".env"虚拟环境 

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

graphrag prompt-tune --root D:\pyprojects\graphrag_project_test_cli   --config D:\pyprojects\graphrag_project_test_cli\settings.yaml --language Chinese --output D:\pyprojects\graphrag_project_test_cli\output-tune2

graphrag index --root D:\pyprojects\graphrag_project_test_cli
 
D:\pyprojects\graphrag\graphrag\index\operations\chunk_text\typing.py [seperator = "seperator"]
D:\pyprojects\graphrag\graphrag\index\operations\chunk_text\strategies.py [def run_seperator]
D:\pyprojects\graphrag\graphrag\index\operations\chunk_text\chunk_text.py [load_strategy]

        case ChunkStrategyType.seperator:
            from graphrag.index.operations.chunk_text.strategies import run_seperator
            return run_seperator


D:\pyprojects\graphrag_project_test\settings.yaml 
        chunks:
        size: 500
        overlap: 100
        group_by_columns: [id]
        type: "seperator"


D:\pyprojects\graphrag\graphrag\config\models\chunking_config.py


class ChunkingConfig(BaseModel):
    """Configuration section for chunking."""

    size: int = Field(description="The chunk size to use.", default=defs.CHUNK_SIZE)
    overlap: int = Field(
        description="The chunk overlap to use.", default=defs.CHUNK_OVERLAP
    )
    group_by_columns: list[str] = Field(
        description="The chunk by columns to use.",
        default=defs.CHUNK_GROUP_BY_COLUMNS,
    )
    
    encoding_model: str | None = Field(
        default=None, description="The encoding model to use."
    )

    strategy: dict | None = Field(
        description="The chunk strategy to use, overriding the default tokenization strategy",
        default={
            "type": ChunkStrategyType.seperator,
            "chunk_size": size,
            "chunk_overlap": overlap,
            "group_by_columns": group_by_columns,
            "encoding_name": encoding_model,
            "seperator": "\n=chunk_delimiter=\n"
        },
    )


    def resolved_strategy(self, encoding_model: str | None) -> dict:
        """Get the resolved chunking strategy."""
        from graphrag.index.operations.chunk_text import ChunkStrategyType

        return self.strategy or {
            "type": ChunkStrategyType.tokens,
            "chunk_size": self.size,
            "chunk_overlap": self.overlap,
            "group_by_columns": self.group_by_columns,
            "encoding_name": encoding_model or self.encoding_model,
        }

