#### SQL Permissions

```
# From docker (Test environment)
GRANT SELECT, UPDATE ON `meteornext-accounts`.`licenses` TO 'meteornext-license'@'172.17.0.%';
GRANT SELECT (id, resources) ON `meteornext-accounts`.`products` TO 'meteornext-license'@'172.17.0.%';
GRANT SELECT ON `meteornext-accounts`.`accounts_sentry` TO 'meteornext-license'@'172.17.0.%';
GRANT SELECT (id, email) ON `meteornext-accounts`.`accounts` TO 'meteornext-license'@'172.17.0.%';

# From lambda-subnet (Prod environment)
GRANT SELECT, UPDATE ON `meteornext-accounts`.`licenses` TO 'meteornext-license'@'10.0.3.%';
GRANT SELECT (id, resources) ON `meteornext-accounts`.`products` TO 'meteornext-license'@'10.0.3.%';
GRANT SELECT ON `meteornext-accounts`.`accounts_sentry` TO 'meteornext-license'@'10.0.3.%';
GRANT SELECT (id, email) ON `meteornext-accounts`.`accounts` TO 'meteornext-license'@'10.0.3.%';
```