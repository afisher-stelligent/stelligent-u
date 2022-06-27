# Questions and answers for Module 02 - S3

## Lab 2.1.2

### Question: Copying to Top Level

How would you copy the contents of the directory to the top level of your bucket?
`aws s3 cp` or `s3 sync`

### Question: Directory Copying

How would you copy the contents and include the directory name in the s3 object paths?
add the `--recursive` flag to the copy command

### Question: Object Access

Can anyone else see your file yet?
Yes. Default is public access.

## Lab 2.2.1

### Question: Downloading Protection

After this, can you download one of your files from the bucket without using your API credentials?
Yes. All are publicly readable

## Lab 2.2.2

### Question: Modify Permissions

How could you use "aws s3 cp" or "aws s3 sync" command to modify the permissions on the file?
Pass the `--acl` flag to the `sync` or `cp` command and use the correct canned policy.

### Question: Changing Permissions

Is there a way you can change the permissions on the file without re-uploading it?

Use `aws s3api` instead of `aws s3` it has more options for working with files already in the bucket.

## Lab 2.2.3

### Question: Reading Policy

What do you see when you try to read the existing bucket policy before you replace it?

You get a `An error occurred (NoSuchBucketPolicy) when calling the GetBucketPolicy operation: The bucket policy does not exist` error.

### Question: Default Permissions

How do the default permissions differ from the policy you're setting?

By default all objects in a bucket are private.
