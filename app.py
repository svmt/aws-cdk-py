#!/usr/bin/env python3

from aws_cdk import core

from pipelines.pipeline_stack import PipelineStack

PIPELINE_ACCOUNT = '997796868421'

app = core.App()
PipelineStack(app, 'PipelineStack')

app.synth()
