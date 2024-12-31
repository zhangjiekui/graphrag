import yaml
import pprint
import asyncio
import graphrag.api as api
from graphrag.index.typing import PipelineRunResult
from graphrag.config.create_graphrag_config import create_graphrag_config
import pandas as pd


import logging
# 设置全局日志级别
logging.basicConfig(level=logging.DEBUG)


pd.options.mode.copy_on_write = True #https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
print=pprint.pprint
project_directory = 'D:\pyprojects\graphrag_project_test'
settings = yaml.safe_load(open(f"{project_directory}/settings.yaml")) 

# print(settings)
# At this point, you can view and modify the imported settings to align with your application's requirements



# Generate a GraphRagConfig object
print("=============Generate a GraphRagConfig object=============")
graphrag_config = create_graphrag_config(
    values=settings, root_dir=project_directory
)

print(graphrag_config)
# pass

# prompt_tune
# prompts = asyncio.run(api.generate_indexing_prompts(config=graphrag_config,root=project_directory,language='Chinese'))

# Build an index
print("=============Build an index=============")
index_result: list[PipelineRunResult] = asyncio.run(api.build_index(config=graphrag_config,is_resume_run=True,memory_profile=True))

# index_result is a list of workflows that make up the indexing pipeline that was run
for workflow_result in index_result:
    status = f"error\n{workflow_result.errors}" if workflow_result.errors else "success"
    print(f"Workflow Name: {workflow_result.workflow}\tStatus: {status}")



# Query an index
print("=============Query an index=============")
import pandas as pd

final_nodes = pd.read_parquet(f"{project_directory}/output/create_final_nodes.parquet")
final_entities = pd.read_parquet(
    f"{project_directory}/output/create_final_entities.parquet"
)
final_communities = pd.read_parquet(
    f"{project_directory}/output/create_final_communities.parquet"
)
final_community_reports = pd.read_parquet(
    f"{project_directory}/output/create_final_community_reports.parquet"
)

text_unit_df = pd.read_parquet(f"{project_directory}/output/create_final_text_units.parquet")
relationship_df = pd.read_parquet(f"{project_directory}/output/create_final_relationships.parquet")

response, context = asyncio.run(api.drift_search(
    config=graphrag_config,
    nodes=final_nodes,
    entities=final_entities,
    community_reports=final_community_reports,
    text_units=text_unit_df,
    relationships=relationship_df,
    community_level=1,
    query="寿县迎河镇中心卫生院信息化系统建设提升项目的建设内容（信息系统或子系统）?",
))

# print(context)
print(response)




# response, context = asyncio.run(api.global_search(
#     config=graphrag_config,
#     nodes=final_nodes,
#     entities=final_entities,
#     communities=final_communities,
#     community_reports=final_community_reports,
#     community_level=2,
#     dynamic_community_selection=False,
#     response_type="Multiple Paragraphs",
#     query="寿县迎河镇中心卫生院信息化系统建设提升项目的建设内容（信息系统或子系统）?",
# ))



# # print(context)
# print(response)