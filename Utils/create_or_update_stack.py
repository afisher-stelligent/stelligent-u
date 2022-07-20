import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
import argparse
import json


def _stack_exists(stack_name):
    stacks = cf.list_stacks().get('StackSummaries')
    for stack in stacks:
        if stack.get('StackStatus') == 'DELETE_COMPLETE':
            continue
        if stack.get('StackStatus') == "ROLLBACK_COMPLETE" or stack.get('StackStatus') == "UPDATE_ROLLBACK_FAILED":
            _cleanup_bad_stack(stack)
            return False
        if stack_name == stack.get('StackName'):
            return True
    return False


def _process_template(template_file):
    with open(template_file) as template:
        template_data = template.read()
    return template_data


def _process_parameters(parameter_file):
    with open(parameter_file) as f:
        data = json.load(f)
    return data


def _cleanup_bad_stack(stack):
    try: 
        resp = cf.delete_stack(StackName=stack.get('StackName'))
        _wait_for_stack(stack.get('StackName'), 'stack_delete_complete')
    except ClientError as error:
        print(f'Stack {stack.get("StackName")} failed to delete')
        raise error

def _wait_for_stack(stack_name, status):
    waiter = cf.get_waiter(stack_name)
    waiter.wait(stack_name, status)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Create or update a stack using AWS CloudFormation')

    arg_parser.add_argument('-n', '--stack_name',       help='Name of the stack to create or update',    required=True)
    arg_parser.add_argument('-t', '--template_file',    help='Path to file in YAML format',              required=True)
    arg_parser.add_argument('-p', '--parameter_file',   help='Parameter file for template parameters.')
    arg_parser.add_argument('-r', '--region',           help='Region to deploy the stack in')
    args = arg_parser.parse_args()

    if args.region: # if a region is not passed, pulls from ENV.
        config = Config(
            region_name = args.region
        )
    
    cf = boto3.client('cloudformation', config=config)
    try:
        if _stack_exists(args.stack_name):
            print(f'Updating {args.stack_name}')
            if args.parameter_file:
                resp = cf.update_stack(
                    StackName=args.stack_name,
                    TemplateBody=_process_template(args.template_file),
                    Parameters=_process_parameters(args.parameter_file),
                    Capabilities=['CAPABILITY_IAM'] # Room for improvement here...
                )
            else:
                resp = cf.update_stack(
                    StackName=args.stack_name,
                    TemplateBody=_process_template(args.template_file),
                    Capabilities=['CAPABILITY_IAM'] # Room for improvement here...
                )
            waiter = cf.get_waiter('stack_update_complete')
        else:
            print(f'Creating {args.stack_name}')
            if args.parameter_file:
                resp = cf.create_stack(
                    StackName=args.stack_name,
                    TemplateBody=_process_template(args.template_file),
                    Parameters=_process_parameters(args.parameter_file),
                    Capabilities=['CAPABILITY_IAM'] # Room for improvement here...
                )
            else:
                resp = cf.create_stack(
                    StackName=args.stack_name,
                    TemplateBody=_process_template(args.template_file),
                    Capabilities=['CAPABILITY_IAM'] # Room for improvement here...
                )

            waiter = cf.get_waiter('stack_create_complete')
            
            print(f'Waiting for stack {args.stack_name} to be ready')
    
        waiter.wait(StackName=args.stack_name)

    except cf.exceptions.ExpiredTokenException as e:
        print("Session Token Expired! Re-run your MFA authentication")
