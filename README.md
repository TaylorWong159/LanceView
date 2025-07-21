# Lance View
A simple LanceDB Viewer

# Author
- Thomas Vu
- Taylor Wong
- Kenny Chau

## Requirements
- Python 3.12+

## Usage
To use the viewer first install the dependencies by running the command:
``` bash
pip install -r requirements.txt
```
Then to start the viewer run
``` bash
./run.sh
```
You can now open the viewer using any browser by going to [http://localhost:8501](http://localhost:8501)
Then simply enter the Database URI and you can start viewing any table in the database

### Using AWS (S3+DynamoDB)
If using S3 (and or DynamoDB) you **MUST** have all the permissions LanceDB requires as your default profile in your credentials file (see [here](https://docs.aws.amazon.com/cli/v1/userguide/cli-configure-files.html) for more details about setting up credentials and configs). If using DynamoDB your default region must match that of the table used
