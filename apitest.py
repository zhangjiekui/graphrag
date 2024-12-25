import graphrag.api as api
from graphrag.index.typing import PipelineRunResult
import yaml

project_directory = 'D:\pyprojects\graphrag_project_test'
settings = yaml.safe_load(open(f"{project_directory}/settings.yaml")) 
print(settings)