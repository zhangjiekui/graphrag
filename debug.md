## VSCode运行调试环境搭建

### 创建虚拟环境并安装包
CTRL + SHIPT + P
> Python:创建虚拟环境
  Venv 在当前工作区中创建".env"虚拟环境 

pip install poethepoet
poetry self add 'poethepoet[poetry_plugin]'



### 调试自己的文件：
点击顶部菜单：运行 -> 添加配置 -> Python 调试程序，当前文件

### 禁用ruff警告 ：
修改D:\pyprojects\graphrag\pyproject.toml
在[tool.ruff]节添加一句line-length = 120
target-version = "py310"
extend-include = ["*.ipynb"]
line-length = 120


## Cli运行测试
graphrag prompt-tune --root D:\pyprojects\graphrag_project_test_cli   --config D:\pyprojects\graphrag_project_test_cli\settings.yaml --language Chinese --output D:\pyprojects\graphrag_project_test_cli\output-tune2

graphrag index --root D:\pyprojects\graphrag_project_test_cli


## 添加按分隔符切分txt文件的代码
切分类型：type = delimiter
切分字串：delimiter_string="\n=chunk_delimiter=\n"

### 
D:\pyprojects\graphrag\graphrag\index\operations\chunk_text\typing.py [delimiter = "delimiter"]
### 方法定义
D:\pyprojects\graphrag\graphrag\index\operations\chunk_text\strategies.py [def run_delimiter]
### 方法调用
D:\pyprojects\graphrag\graphrag\index\operations\chunk_text\chunk_text.py [load_strategy]

        case ChunkStrategyType.delimiter:
            from graphrag.index.operations.chunk_text.strategies import run_delimiter
            return run_delimiter

### 相关配置
D:\pyprojects\graphrag_project_test\settings.yaml 
        type: "delimiter"
D:\pyprojects\graphrag\graphrag\config\defaults.py
        CHUNK_DELIMITER_STRING = "\n=chunk_delimiter=\n"

D:\pyprojects\graphrag\graphrag\config\models\chunking_config.py
    class ChunkingConfig(BaseModel):
        type: str | None = Field(default=ChunkStrategyType.delimiter, description="The chunking method to use. Values:ChunkStrategyType.delimiter|tokens|sentence Default: delimiter")
        delimiter_string: str | None = Field(default=defs.CHUNK_DELIMITER_STRING, description="The delimiter_string to use as text.split(delimiter_string).")

        def resolved_strategy(self, encoding_model: str | None) -> dict:
            """Get the resolved chunking strategy."""
            from graphrag.index.operations.chunk_text import ChunkStrategyType

            return self.strategy or {
                "type": self.type or ChunkStrategyType.tokens,
                "chunk_size": self.size,
                "chunk_overlap": self.overlap,
                "delimiter_string": self.delimiter_string,
                "group_by_columns": self.group_by_columns,
                "encoding_name": encoding_model or self.encoding_model,

D:\pyprojects\graphrag_project_test_cli\settings.yaml
    chunks:
        size: 500
        overlap: 100
        group_by_columns: [id]
        type: "delimiter"
        delimiter_string: "\n=chunk_delimiter=\n"

    

## todo 定义tokens方法

    计划使用大模型自身的tokens接口 http://10.1.150.105:9997/doc
    比较了一段文本，结果差别挺大的：
        qwen25b70  427
        cl100k_base 870

## 源码走读

### D:\pyprojects\graphrag\graphrag\cli\main.py
#### _initialize_cli  -> graphrag\cli\initialize.py 文件中的 def initialize_project_at(path: Path) 方法
    https://vscode.dev/github/zhangjiekui/graphrag/blob/main/graphrag/cli/initialize.py#L28

#### _prompt_tune_cli -> api.generate_indexing_prompts -> prompt_tune.py 文件中的  async def generate_indexing_prompts

#### _index_cli -> -> api.build_index -> graphrag\api\index.py 文件中的 async def build_index
    https://vscode.dev/github/zhangjiekui/graphrag/blob/main/graphrag/api/index.py#L23
##### 注意--resume参数
    graphrag index --root D:\pyprojects\graphrag_project_test_cli --verbose --memprofile  --resume true
    asyncio.run(api.build_index(config=graphrag_config,is_resume_run=True,memory_profile=True))
##### update_cli 其实也是最终调用async def build_index


## 流程执行顺序：
### 为体验和调试全部功能，需将D:\pyprojects\graphrag\graphrag\config\defaults.py 中的False替换为True

INFO:graphrag.index.workflows.load:Workflow Run Order: 
['create_base_text_units', 'create_final_documents', 'extract_graph', 'create_final_covariates', 'compute_communities', 'create_final_entities', 'create_final_relationships', 'create_final_communities', 'create_final_nodes', 'create_final_text_units', 'create_final_community_reports', 'generate_text_embeddings']

### create_base_text_units  -> graphrag\index\workflows\v1\create_base_text_units.py
### create_final_documents  -> graphrag\index\workflows\v1\create_final_documents.py



## 与R2R结合

### Ingestion Provider
https://github.com/SciPhi-AI/R2R/blob/main/py/core/providers/ingestion/r2r/base.py
https://r2r-docs.sciphi.ai/documentation/configuration/ingestion

### R2R Core和Services(或许可以跳过 )
[R2R库->py->core目录]关键是实现了Postgres 向量和图数据库 https://github.com/SciPhi-AI/R2R/blob/main/py/core/database/postgres.py
[R2R库->services目录]以及Leiden  cluster_graph： https://github.com/SciPhi-AI/R2R/blob/main/services/clustering/main.py

### 在GraphRag代码库中使用R2R API & SDK在GraphRag中增加一套平行的lancedb和parquet存储的代码实现（但可以保留缓存部分）