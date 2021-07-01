from aws_cdk import core

from .pipelines_vpc_stack import PipelinesVpcStack


class VPCStage(core.Stage):
  def __init__(self, scope: core.Construct, id: str,  **kwargs):
    super().__init__(scope, id, **kwargs)

    PipelinesVpcStack(self, 'VpcStack')
