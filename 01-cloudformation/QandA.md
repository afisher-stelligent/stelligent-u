# Q and A for Module 01

## Retrospective 1.1

### Question: Why YAML

* Why do we prefer the YAML format for CFN templates?

YAML is much more conscise and easier to read than JSON.

### Question: Protecting Resources

* What else can you do to prevent resources in a stack from being deleted?
  1. Use IAM policies to prevent users from having the ability to delete stacks
  2. Use the `DeletionPolicy` Attribute in the template itself
  3. Use Stack Policies to prevent individual resources from being deleted or updated
* How is that different from applying Termination Protection?
    These are different, more fine-grained ways of protecting stacks and their resources,
    whether it be at the user level or the resource level.

### Task: String Substitution

Demonstrate 2 ways to code string combination/substitution using built-in CFN functions.

String concatenation/Substitution can be achived via `!Join` or `!Sub`

`!Join ["-", [!Ref "BucketNameParameter", !Ref AWS::AccountId]]`

``` yaml
    !Sub 
    - 'www.${DomainName}'
    - DomainName: !Ref MyCoolSite
```
