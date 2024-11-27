# Samsung Pass .spass decoder

The Samsung Pass password manager app has the ability to export the stored data into _a file_.

But there doesn't seem to be any way to read it, at least judging by the countless forum posts of people asking for help.

This tool is an attempt to remedy this and help people move their data around without obstacles - especially if you don't want to stay with their app for one reason or the other.

## Encryption parameters: 

With some guessing, trial and error this is what I've managed to figure out, and it seems to work

- **Salt Size:** 20 bytes
- **Iteration Count:** 70,000
- **Key Length:** 256 bits
- **Key Derivation Algorithm:** PBEwithHmacSHA256AndAES_128
- **Cipher Algorithm:** AES/CBC/PKCS5Padding
- **IV Size:** Determined by the AES block size (typically 16 bytes for AES)
- **Encoding:** Base64

If you don't have the actual password which was used to encrypt the exported `.spass` file, then this tool won't help you.

## File contents

This is what the file looks like on-disk

```text
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
```

## File format

Once decrypted, this is what the base64 AES contains inside.

```csv
22                  # Format version, I guess?
true;true;true;true # Which options you selected when exporting.
next_table          # Table delimiter
_id;origin_url;action_url;username_element;username_value;id_tz_enc;password_element;password_value;pw_tz_enc;host_url;ssl_valid;preferred;blacklisted_by_user;use_additional_auth;cm_api_support;created_time;modified_time;title;favicon;source_type;app_name;package_name;package_signature;reserved_1;reserved_2;reserved_3;reserved_4;reserved_5;reserved_6;reserved_7;reserved_8;credential_memo;otp
NA==;aHR0cHM6Ly9Hb29nbGUuY29t;JiYmTlVMTCYmJg==;JiYmTlVMTCYmJg==;dXNlcjMz;JiYmTlVMTCYmJg==;JiYmTlVMTCYmJg==;cGFzczMz;JiYmTlVMTCYmJg==;aHR0cHM6Ly9Hb29nbGUuY29tLw==;MA==;MA==;MA==;JiYmTlVMTCYmJg==;JiYmTlVMTCYmJg==;MTczMjY5Mjk2MjI0Mw==;MTczMjY5Mjk2MzQ2Mw==;Z29vZ2xlLmNvbQ==;;Mw==;JiYmTlVMTCYmJg==;JiYmTlVMTCYmJg==;JiYmTlVMTCYmJg==;JiYmTlVMTCYmJg==;JiYmTlVMTCYmJg==;JiYmTlVMTCYmJg==;JiYmTlVMTCYmJg==;JiYmTlVMTCYmJg==;JiYmTlVMTCYmJg==;JiYmTlVMTCYmJg==;JiYmTlVMTCYmJg==;;JiYmTlVMTCYmJg==
next_table          # Table delimiter
_id;card_number_encrypted;first_six_digit;last_four_digit;name_on_card;expiration_month;expiration_year;billing_address_id;vault_status;date_modified;reserved_4;reserved_5;reserved_6
MQ==;MTExMTIyMjIzMzMzNDY3NQ==;MTExMTIy;NDY3NQ==;ZHVtbXk=;MTE=;MjY=;MA==;NA==;MTczMjczNzU5MDg2NA==;;ZHVtbXlrYXJk;
next_table          # Table delimiter
_id;full_name;company_name;street_address;city;state;zipcode;country_code;phone_number;email;date_modified;reserved_4;reserved_5;reserved_6
MQ==;ZHVtbXk=;bm9kZXRhaWxz;ZHVtbXlzdHJlZXQ=;QUNpdHk=;;MTM1Nw==;SFI=;MTk0NjI4NDk3Ng==;c2tpcEBleGFtcGxlLmNvbQ==;MTczMjczNzU4ODk4OA==;;;eyJjb3VudHJ5Q29kZSI6IkhSIiwibGlzdEFkZHJlc3MiOlt7ImFkZHJlc3NWaWV3RmllbGQiOnsiYXBwTGFiZWwiOiJOYW1lIiwiZmllbGQiOiJSRUNJUElFTlQiLCJpc0Ryb3BEb3duIjpmYWxzZX0sImNvbHVtbk5hbWUiOiJmdWxsX25hbWUifSx7ImFkZHJlc3NWaWV3RmllbGQiOnsiYXBwTGFiZWwiOiJEZXRhaWxzIiwiZmllbGQiOiJPUkdBTklaQVRJT04iLCJpc0Ryb3BEb3duIjpmYWxzZX0sImNvbHVtbk5hbWUiOiJjb21wYW55X25hbWUifSx7ImFkZHJlc3NWaWV3RmllbGQiOnsiYXBwTGFiZWwiOiJTdHJlZXQgYWRkcmVzcyIsImZpZWxkIjoiQUREUkVTU19MSU5FXzEiLCJpc0Ryb3BEb3duIjpmYWxzZX0sImNvbHVtbk5hbWUiOiJzdHJlZXRfYWRkcmVzcyJ9LHsiYWRkcmVzc1ZpZXdGaWVsZCI6eyJhcHBMYWJlbCI6IlBvc3RhbCBjb2RlIiwiZmllbGQiOiJQT1NUQUxfQ09ERSIsImlzRHJvcERvd24iOmZhbHNlfSwiY29sdW1uTmFtZSI6InppcGNvZGUifSx7ImFkZHJlc3NWaWV3RmllbGQiOnsiYXBwTGFiZWwiOiJDaXR5IiwiZmllbGQiOiJMT0NBTElUWSIsImlzRHJvcERvd24iOmZhbHNlfSwiY29sdW1uTmFtZSI6ImNpdHkifV0sImxvY2FsZSI6ImVuZyIsInZlcnNpb25Db2RlIjo1fQ==
next_table          # Table delimiter
_id;note_title;note_detail;date_modified
MQ==;YW5vdGhlciBub3Rl;ZHVtZHVt;MTczMjczNzYwMzUwMQ==
```

This is the general structure of the encrypted content. It's just a CSV with colum data base64 encoded.