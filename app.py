#!/usr/bin/env python3

from aws_cdk import core

from pipelines.pipeline_stack import PipelineStack

PIPELINE_ACCOUNT = '045670552235'

app = core.App()
PipelineStack(app, 'PipelineStack', env={
  'account': PIPELINE_ACCOUNT,
  'region': 'eu-central-1',
})

app.synth()
