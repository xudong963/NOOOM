## DatabendCloud

[Apply for a free trial](https://databend.com/apply)

## bendsql
https://github.com/datafuselabs/bendsql

## Config

```
export BENDSQL_DSN="databend://<user>:<pwd>@<host>:443/<database>"
```

## Prepare
[prepare.sql](prepare.sql)

## Run

```
python3 ./spill.py [--database <database>] [--ratio <memoryratio>]
```

* `--ratio`: join spilling memory ratio, range:[0, 100), zero means unlimited.
