# Q & A

These are the answers to the questions posed by the labs for module 00-dev-environment

## Question 0.1.1: 1

### What method did you use to store the aws credentials? What are some other options?

I wrote a Python3 script that does the following:

* Prompt the user for an MFA code and validate it
* Store the credentials in `~/.aws/credentials`
* Print a message at the end that explains the various ways the credential can be accessed.

The credentials can be stored as environment variables, or as a profile that can used via the `--profile` flag within aws CLI commands.

## Question 0.1.1: 2

### Which AWS environment variable cannot be set in order to run the aws sts get-session-token command?

The `AWS_SESSION_TOKEN` environment variable.

## Retrospective 0.1

## Question: Environments

### Running the two commands in lab 0.1.1 and lab 0.1.3 should have shown the same results. What does this tell you about the access the keys give you on your laptop and the access you have in the Cloud9 environment?

The IAM user has access to the same things as the keys provided to the laptop.

### What other methods are there to provide this level of access without using keys?

You could use STS AssumeRole to assume the role that a given IAM user has. This would provide the same level of access.
