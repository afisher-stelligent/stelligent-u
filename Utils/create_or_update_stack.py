import boto3
from botocore.config import Config

import argparse
import json


def _stack_exists(stack_name):
    stacks = cf.list_stacks().get('StackSummaries')
    for stack in stacks:
        if stack.get('StackStatus') == 'DELETE_COMPLETE':
            continue
        if stack_name == stack.get('StackName'):
            return True
    return False


def _process_template(template_file):
    with open(template_file) as template:
        template_data = template.read()
    return template_data


def _process_parameters(parameter_file):
    with open(args.parameter_file) as f:
        data = json.load(f)
    return data

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Create or update a stack using AWS CloudFormation')

    arg_parser.add_argument('-n', '--stack_name',       help='Name of the stack to create or update',    required=True)
    arg_parser.add_argument('-t', '--template_file',    help='Path to file in YAML format',              required=True)
    arg_parser.add_argument('-p', '--parameter_file',   help='Parameter file for template parameters.',  required=True)
    arg_parser.add_argument('-r', '--region',           help='Region to deploy the stack in',            required=True)
    args = arg_parser.parse_args()

    config = Config(
        region_name = args.region
    )
    
    cf = boto3.client('cloudformation', config=config)

    if _stack_exists(args.stack_name):
        print(f'Updating {args.stack_name}')
        resp = cf.update_stack(
            StackName=args.stack_name,
            TemplateBody=_process_template(args.template_file),
            Parameters=_process_parameters(args.parameter_file),
            Capabilities=['CAPABILITY_IAM']
        )
        waiter = cf.get_waiter('stack_update_complete')
    else:
        print(f'Creating {args.stack_name}')
        resp = cf.create_stack(
            StackName=args.stack_name,
            TemplateBody=_process_template(args.template_file),
            Parameters=_process_parameters(args.parameter_file),
            Capabilities=['CAPABILITY_IAM']
        )
        waiter = cf.get_waiter('stack_create_complete')
        
        print(f'Waiting for stack {args.stack_name} to be ready')
    
    waiter.wait(StackName=args.stack_name)