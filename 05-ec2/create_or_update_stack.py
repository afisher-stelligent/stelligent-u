import boto3
import argparse
import yaml
import json


cf = boto3.client('cloudformation')

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
    return cf.validate_template(TemplateBody=template_data)


def _process_parameters(parameter_file):
    with open(parameter_file) as parameters:
        parameter_data = json.load(parameters)
    return parameter_data

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Create or update a stack using AWS CloudFormation')

    arg_parser.add_argument('-n', '--stack_name',       description='Name of the stack to create or update',    required=True)
    arg_parser.add_argument('-t', '--template_file',    description='Path to file in YAML format',              required=True)
    arg_parser.add_argument('-p', '--parameter_file',   description='Parameter file for template parameters.',  required=True)
    args = arg_parser.parse_args()

    params = {
        'StackName': args.stack_name,
        'TemplateBody': _process_template(args.template_file),
        'Parameters': _process_parameters(args.parameter_file),
    }    
    if _stack_exists(args.stack_name):
            print(f'Updating {args.stack_name}')
            stack_result = cf.update_stack(**params)
            waiter = cf.get_waiter('stack_update_complete')
    else:
        print(f'Creating {args.stack_name}')
        stack_result = cf.create_stack(**params)
        waiter = cf.get_waiter('stack_create_complete')
        
        print("...waiting for stack to be ready...")
        waiter.wait(StackName=args.stack_name)