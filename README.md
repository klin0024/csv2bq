# csv2bq.py 參數說明

Var           | Value                                         | Description
:-------------|:----------------------------------------------|:------------------------
--project	  | gcp-expert-sandbox-allen	                  | 專案名稱
--region	  | us-central1	                                  | 地區名稱
--credential  | gcp-expert-sandbox-allen-c1fcfd19238a.json	  | 憑據檔案名稱
--temp_bucket | gcp-expert-sandbox-allen-temp_bucket	      | 暫存bucket名稱
--input	      | gs://gcp-expert-sandbox-allen/folder/data.csv | 輸入的CSV位置
--output	  | gcp-expert-sandbox-allen:dataset.table	      | 輸出bq的表
--schema	  | '{"admit":"FLOAT",<br>"gre":"FLOAT",<br>"gpa":"FLOAT",<br>"rank":"FLOAT"}' | schema json

# csv2bq.py 使用說明

pip3 install -r requirements.txt

python3 csv2bq.py --project=gcp-expert-sandbox-allen \\<br>
--region=us-central1 \\<br>
--credential=gcp-expert-sandbox-allen-c1fcfd19238a.json \\<br>
--temp_bucket=gcp-expert-sandbox-allen-temp_bucket \\<br>
--input=gs://gcp-expert-sandbox-allen/folder/data.csv \\<br>
--output=gcp-expert-sandbox-allen:dataset.table \\<br>
--schema='{"admit":"FLOAT","gre":"FLOAT","gpa":"FLOAT","rank":"FLOAT"}'



# csv2bq-part.py 參數說明

Var           | Value                                         | Description
:-------------|:----------------------------------------------|:------------------------
--project	  | gcp-expert-sandbox-allen	                  | 專案名稱
--region	  | us-central1	                                  | 地區名稱
--credential  | gcp-expert-sandbox-allen-c1fcfd19238a.json	  | 憑據檔案名稱
--temp_bucket | gcp-expert-sandbox-allen-temp_bucket	      | 暫存bucket名稱
--input	      | gs://gcp-expert-sandbox-allen/folder/data.csv | 輸入的CSV位置
--output	  | gcp-expert-sandbox-allen:dataset.table	      | 輸出bq的表
--schema	  | '{"admit":{"enabled":1,"type":"FLOAT"},<br>"gre":{"enabled":1,"type":"FLOAT"},<br>"gpa":{"enabled":0,"type":"FLOAT"},<br>"rank":{"enabled":1,"type":"FLOAT"}}' | schema json,可以選擇是否要輸出到bq

# csv2bq-part.py 使用說明

pip3 install -r requirements.txt

python3 csv2bq-part.py --project=gcp-expert-sandbox-allen \\<br>
--region=us-central1 \\<br>
--credential=gcp-expert-sandbox-allen-c1fcfd19238a.json \\<br>
--temp_bucket=gcp-expert-sandbox-allen-temp_bucket \\<br>
--input=gs://gcp-expert-sandbox-allen/folder/data.csv \\<br>
--output=gcp-expert-sandbox-allen:dataset.table \\<br>
--schema='{"admit":{"enabled":1,"type":"FLOAT"},"gre":{"enabled":1,"type":"FLOAT"},"gpa":{"enabled":0,"type":"FLOAT"},"rank":{"enabled":1,"type":"FLOAT"}}'