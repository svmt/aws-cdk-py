from aws_cdk import core
from aws_cdk import aws_codepipeline as codepipeline
from aws_cdk import aws_codepipeline_actions as cpactions
from aws_cdk import pipelines
import boto3

from .vpc_stage import VPCStage


class PipelineStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        source_artifact = codepipeline.Artifact()
        cloud_assembly_artifact = codepipeline.Artifact()

        pipeline = pipelines.CdkPipeline(
            self, 'Pipeline',
            cloud_assembly_artifact=cloud_assembly_artifact,
            pipeline_name='VpcPipeline',

            source_action=cpactions.GitHubSourceAction(
                action_name='GitHub',
                output=source_artifact,
                oauth_token=core.SecretValue.secrets_manager('github-token'),
                owner=self.node.try_get_context("github_alias"),
                repo=self.node.try_get_context("github_repo_name"),
                trigger=cpactions.GitHubTrigger.POLL),

            synth_action=pipelines.SimpleSynthAction(
                source_artifact=source_artifact,
                cloud_assembly_artifact=cloud_assembly_artifact,
                install_command='npm install -g aws-cdk && pip install -r requirements.txt',
                build_command='pytest unittests',
                synth_command='cdk synth'))

        #boto3.setup_default_session(profile_name='cicd')
        session = boto3.Session(profile_name='cicd')
        organization = session.client('organizations')
        paginator = organization.get_paginator('list_accounts')
        page_iterator = paginator.paginate()

        account_list = []
        stages = (
            'Dev',
            'Staging',
            'Prod',
        )

        for page in page_iterator:
            for acct in page['Accounts']:
                if not acct['Name'] in stages:
                    continue
                account_list.append(acct)  # print the account

        for account in account_list:
            pipeline.add_application_stage(VPCStage(self, account['Name'], env={
                'account': account['Id'],
                'region': 'eu-central-1',
            }))
