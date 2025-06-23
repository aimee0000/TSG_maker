# [Title] Support for multiple chips on the same uC.

## Problem Phenomenon (The issue):
The library is designed to support only a single WIZ chip on a microcontroller due to namespace collisions that occur during reading and writing operations.

## Cause (The cause of the issue):
The namespace collisions are caused by the implementation of the library, which uses global variables or names that conflict when attempting to support multiple WIZ chips simultaneously.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
Duplicate the library files and rename the global variables or any conflicting names to ensure they are unique for each WIZ chip being used on the microcontroller. This approach avoids namespace collisions and allows support for multiple chips.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/144)


# [Title] It occurs Global memory Buffer Overrun

## Problem Phenomenon (The issue):
A global memory buffer overrun occurs due to an incorrect check on socket numbers in the `socket()` function. The macro `CHECK_SOCKNUM()` incorrectly allows a socket number of 4, which leads to accessing an out-of-bounds index in the `sock_pack_info` array, which has a size of 4.

## Cause (The cause of the issue):
The macro `CHECK_SOCKNUM()` was incorrectly defined as `if(sn > _WIZCHIP_SOCK_NUM_) return SOCKERR_SOCKNUM;`. This logic erroneously allows the socket number to be 4, leading to potential memory access issues because the `sock_pack_info` array only accommodates indices 0 through 3.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
The issue was solved by modifying the macro definition to correctly check the socket number using `if(sn >= _WIZCHIP_SOCK_NUM_) return SOCKERR_SOCKNUM;`. This change ensures that any socket number greater than or equal to the size of the `sock_pack_info` array is not allowed, thus preventing the buffer overrun. The fix has already been implemented in the codebase, as indicated in the comments.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/140)


# [Title] cannot access documentation

## Problem Phenomenon (The issue):
The user is unable to access the documentation linked in the README. Attempts to open the documentation using Windows' hh.exe result in a blank display. Additionally, using various e-book readers has not worked, and the user is unable to find a PDF or other format of the documentation online.

## Cause (The cause of the issue):
The issue is likely related to the way Windows handles CHM (Compiled HTML Help) files, which can result in them appearing blank due to security settings or file properties.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
The solution involves adjusting Windows settings to properly display CHM files. Here is a potential step-by-step guide based on the provided comment link:
1. Right-click on the CHM file and select "Properties."
2. In the Properties window, look for an "Unblock" button or checkbox near the bottom. If present, click it to unblock the file.
3. Apply the changes and close the Properties window.
4. Try opening the CHM file again using hh.exe or another compatible viewer.

For more detailed guidance, refer to the linked community discussion: [Spiceworks Community Solution](https://community.spiceworks.com/topic/1961503-solved-windows-10-chm-help-files-showing-up-blank).

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/131)


# [Title] DNS is not cleared after RSTn is triggered for a WIZ550io or WIZ850io

## Problem Phenomenon (The issue):
After resetting the device using the RSTn pin, the `wizchip_getnetinfo()` function returns all IP addresses as 0, except for the DNS IP address, when using Espruino with PICO.

## Cause (The cause of the issue):
The issue might originate from the specific handling of network configurations in the Espruino environment after a hardware reset, which causes the IP addresses to not be correctly re-initialized or retrieved, except for the DNS IP.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
The issue has been fixed specifically for Espruino, as indicated by the comment. For a detailed solution, one might need to refer to the changes made in the Espruino environment or the relevant library updates. If the issue persists, checking for updates or patches in the Espruino firmware or related networking libraries may be necessary.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/100)


# [Title] 请问对于双W5500网口的支持, 该库是否支持?

## Problem Phenomenon (The issue):
The current library only supports one chip.

## Cause (The cause of the issue):
The library is configured to work with only a single chip, and it does not have built-in support for handling multiple chips simultaneously.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
Reconfigure the library by adding the chip ID to the function parameters within the library. Alternatively, use the library for each chip separately but modify the function names to ensure they do not conflict with each other.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/90)


# [Title] setSn_PROTOR(sn, proto) error

## Problem Phenomenon (The issue):
There is an issue in the `w5300.h` file within the `ioLibrary_Driver` repository on GitHub, specifically at line 2128. The current code does not correctly handle protocol settings due to incorrect bit manipulation.

## Cause (The cause of the issue):
The cause of the issue is improper bit masking and assignment in the function that sets the protocol in the W5300 chip. The existing implementation does not correctly preserve the higher byte of the protocol register while setting the lower byte.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
The solution is to modify the line of code as follows to ensure correct bit manipulation:
```c
WIZCHIP_WRITE(Sn_PROTOR(sn), (WIZCHIP_READ(Sn_PROTOR(sn)) & 0xFF00) | (((uint16_t)proto) & 0x00FF))
```
Additionally, review and correct any other related incorrect bit manipulations in the `W5300.h` file, as noted by the commenter.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/82)


# [Title] Passive FTP not working

## Problem Phenomenon (The issue):
When using passive FTP mode with the W5500 FTP server, the connection setup works initially. However, during the execution of the "case STOR_CMD", the code attempts to connect to the remote IP address 0.0.0.0. This indicates that the passive FTP implementation does not correctly store the IP address of the FTP client before attempting to connect the data socket.

## Cause (The cause of the issue):
The issue arises because the passive FTP implementation on the W5500 server fails to record the client's IP address properly. As a result, when attempting to open a data connection, it defaults to the IP address 0.0.0.0, which is incorrect.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
To resolve the issue, ensure that the passive FTP implementation correctly stores the client's IP address before the data socket connection attempt. This may involve modifying the code around line 872 in `ftpd.c` to ensure that the correct client IP address is used.

Additionally, ensure that your FTP client is set up correctly to use passive mode by calling `session.set_pasv(True)` when initializing the FTP session in your client code. However, remember that the primary fix needs to be on the server-side code to handle the client's IP address correctly.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/81)


# [Title] NibbleToHex() missing in send_DHCP_DISCOVER()

## Problem Phenomenon (The issue):
The issue is that line 383 in `dhcp.c` is missing a conversion from hex to ASCII, resulting in the MAC address displaying as weird characters in the router if the MAC address is not within the readable ASCII range.

## Cause (The cause of the issue):
The cause of the issue is the lack of conversion from hexadecimal to ASCII for the MAC address in the specified line of the `dhcp.c` file.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
The solution involved updating the code to include the necessary conversion from hex to ASCII for the MAC address at line 383 in `dhcp.c`. The update was completed, as confirmed in the comments.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/77)


# [Title] 107行和110行重复了

## Problem Phenomenon (The issue):
There is an issue related to the `httpParser.c` file in the `ioLibrary_Driver` repository, specifically at line 110, which might be causing unexpected behavior in the HTTP server functionality.

## Cause (The cause of the issue):
The exact cause is not detailed in the issue content provided, but it is likely related to the code implementation at line 110 in the `httpParser.c` file, which may have a bug or incorrect logic affecting the HTTP server operations.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
The solution would involve reviewing and potentially modifying the code at line 110 in `httpParser.c` to address the issue. Specific changes are not provided in the issue content, so it would require further investigation into the code logic and functionality to implement a fix.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/74)


# [Title] sn范围在(0<=n<=7)

## Problem Phenomenon (The issue):
The issue concerns the value of the `_WIZCHIP_SOCK_NUM_` in the `wizchip_conf.h` file, which may be causing unexpected behavior in the Ethernet socket functionality.

## Cause (The cause of the issue):
The problem arises from incorrect assumptions or misconfigurations regarding the `_WIZCHIP_SOCK_NUM_` value. This value should be set to either '8' or '4', depending on the specific hardware configuration.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
Ensure that the `_WIZCHIP_SOCK_NUM_` in the `wizchip_conf.h` file is correctly defined as either '8' or '4'. This setting should reflect the correct number of sockets supported by the hardware being used. To resolve the issue:
1. Open the `wizchip_conf.h` file in your project.
2. Locate the definition of `_WIZCHIP_SOCK_NUM_`.
3. Confirm that it is set to the appropriate value ('8' or '4') based on your hardware specifications.
4. Save the changes and recompile the project to ensure the updated configuration is applied.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/73)


# [Title] fix ifdef and brackets in Internet/DNS/dns.c

## Problem Phenomenon (The issue):
The issue involves a small problem with a debugging feature related to DNS. Specifically, there is a typo in the code where the macro `_DNS_DEUBG_` is used instead of the correct `_DNS_DEBUG_`. This typo prevents the debugging message from being printed correctly.

## Cause (The cause of the issue):
The cause of the issue is a typographical error in the code. The macro `_DNS_DEUBG_` is incorrectly spelled and should be `_DNS_DEBUG_`. This typo leads to the conditional compilation not working as intended, thereby not printing the necessary debugging message.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
The solution involves correcting the typographical error in the code by replacing `_DNS_DEUBG_` with `_DNS_DEBUG_`. The following changes should be made in the `dns.c` file:

```diff
diff --git a/Internet/DNS/dns.c b/Internet/DNS/dns.c
index 9f7107b..449ac0a 100644
--- a/Internet/DNS/dns.c
+++ b/Internet/DNS/dns.c
@@ -367,8 +367,8 @@ int8_t parseDNSMSG(struct dhdr * pdhdr, uint8_t * pbuf, uint8_t * ip_from_dns)
 	for (i = 0; i < pdhdr->qdcount; i++)
 	{
 		cp = dns_question(msg, cp);
-   #ifdef _DNS_DEUBG_
-      printf("MAX_DOMAIN_NAME is too small, it should be redfine in dns.h"
+   #ifdef _DNS_DEBUG_
+      printf("MAX_DOMAIN_NAME is too small, it should be redfine in dns.h");
    #endif
 		if(!cp) return -1;
 	}
@@ -377,8 +377,8 @@ int8_t parseDNSMSG(struct dhdr * pdhdr, uint8_t * pbuf, uint8_t * ip_from_dns)
 	for (i = 0; i < pdhdr->ancount; i++)
 	{
 		cp = dns_answer(msg, cp, ip_from_dns);
-   #ifdef _DNS_DEUBG_
-      printf("MAX_DOMAIN_NAME is too small, it should be redfine in dns.h"
+   #ifdef _DNS_DEBUG

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/69)


# [Title] strindex unused

## Problem Phenomenon (The issue):
Compiler warnings are generated in the `MQTTFormat.c` file due to the unused variable `strindex` in the functions `MQTTFormat_toClientString` and `MQTTFormat_toServerString`.

## Cause (The cause of the issue):
The variable `strindex` is declared and assigned a value in both functions but is never utilized, leading to the compiler generating warnings about the variable being set but not used.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
To resolve the compiler warnings, remove the declaration and assignment of the unused variable `strindex` from both functions `MQTTFormat_toClientString` and `MQTTFormat_toServerString` in the `MQTTFormat.c` file. This can be done by deleting or commenting out the following lines:

For `MQTTFormat_toClientString`:
```c
int strindex = 0;
```

For `MQTTFormat_toServerString`:
```c
int strindex = 0;
```

Ensure that removing these lines does not affect any other logic in the functions. If the variable is intended for future use or debugging, consider commenting out the lines instead of deleting them completely.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/66)


# [Title] type can be returned unitialized

## Problem Phenomenon (The issue):
A warning is generated in the `parseDHCPMSG` function of the `dhcp.c` file, indicating that the variable `type` may be used uninitialized. This warning suggests potential undefined behavior if the variable `type` is accessed before being properly initialized.

## Cause (The cause of the issue):
The cause of the issue is that the variable `type` is declared but not explicitly initialized before it is potentially returned in the `parseDHCPMSG` function. If the logic of the function does not set a value to `type` before it is returned, it leads to the warning and possible undefined behavior.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
To resolve the issue, ensure that the variable `type` is initialized before it is used. This can be done by assigning a default value to `type` at the time of declaration. For example, modify the code to initialize `type` as follows:

```c
int type = DEFAULT_VALUE; // Replace DEFAULT_VALUE with an appropriate default value
```

Alternatively, ensure that all code paths within the function assign a value to `type` before it is returned. This might include setting a value to `type` at various points in the function logic where it is expected to be used.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/64)


# [Title] unused variables warning for _WIZCHIP_ >= W5200

## Problem Phenomenon (The issue):
An unused variable warning is generated when using chips outside the range specified by the `#if _WIZCHIP_ < W5200` macro in the `wizchip_conf.c` file.

## Cause (The cause of the issue):
The variable `j` is declared and used only within the `#if _WIZCHIP_ < W5200` macro. When the code is compiled for chips that do not meet this condition, the variable `j` is not utilized, leading to an unused variable warning.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
To resolve the unused variable warning, ensure that the variable `j` is declared only within the scope where it is used. Place the declaration of `j` inside the `#if _WIZCHIP_ < W5200` block, so it is only declared when necessary. This prevents the warning when compiling for chips outside this range. Here is a step-by-step guide:

1. Open the `wizchip_conf.c` file in your code editor.
2. Locate the code block where the variable `j` is declared.
3. Move the declaration of `j` inside the `#if _WIZCHIP_ < W5200` macro block.
4. Ensure the variable is only declared and used within this conditional compilation block.
5. Save the changes and recompile the code. The unused variable warning should no longer appear for chips outside the specified range.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/62)


# [Title] many compiler warnings in mqtt_interface

## Problem Phenomenon (The issue):
The user experiences multiple compiler warnings while using gcc version 5.4.0 on Ubuntu 16.04. These warnings occur in the `mqtt_interface.c` file of the MQTT library and include implicit function declarations and control reaching the end of non-void functions without returning a value. Additionally, there is a warning about differing pointer signedness in a function argument.

## Cause (The cause of the issue):
1. **Implicit Function Declarations**: The warnings about implicit declarations of functions such as `recv`, `send`, `disconnect`, `socket`, and `connect` suggest that the appropriate headers where these functions are declared are not included in the source file.
2. **Control Reaches End of Non-Void Function**: The functions `w5x00_read`, `w5x00_write`, and `ConnectNetwork` must return a value as they are non-void, yet the code reaches the end of these functions without returning a value.
3. **Pointer Signedness**: The warning about differing signedness in the `connect` function suggests a mismatch between the expected and actual argument types, likely involving the `ip` variable.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
1. **Include Necessary Headers**: Add the necessary headers for the socket functions to the top of the `mqtt_interface.c` file. This typically includes:
   ```c
   #include <sys/types.h>
   #include <sys/socket.h>
   #include <netinet/in.h>
   #include <arpa/inet.h>
   #include <unistd.h>
   ```

2. **Return Appropriate Values**: Ensure that all non-void functions return a value. Modify the `w5x00_read`, `w5x00_write`, and `ConnectNetwork` functions to return appropriate values. For example:
   ```c
   int w5x00_read(Network* n, unsigned char* buffer, int len) {
       return recv(n->my_socket, buffer, len);
   }
   ```

3. **Fix Pointer Signedness**: Ensure that the data types match the expected types in function calls. For the `connect` function, ensure that the `ip` variable is of the correct type. If `ip` is of type `unsigned char*`, you may need to cast it to `const char

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/59)


# [Title] Problem with extern "C" encoding of quotation marks

## Problem Phenomenon (The issue):
In header files (.h files), the `extern "C"` statement is incorrectly encoded as `extern ¡°C¡±`, causing issues with the encoding of quotation marks.

## Cause (The cause of the issue):
The issue is caused by incorrect encoding of the quotation marks in the `extern "C"` statement within the header files.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
Correct the encoding of the quotation marks in the header files to ensure that `extern "C"` is properly formatted. This may involve changing the text encoding settings or manually replacing the incorrect quotation marks with standard double quotation marks in the code editor or IDE being used.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/57)


# [Title] See I have a problem with the code display or download, for ioLibrary_Driver/Ethernet/wizchip_conf.h

## Problem Phenomenon (The issue):
The issue is that some lines of code are missing the `//!` comment marker, which is used to indicate non-functional descriptive text or comments in the code. This inconsistency might lead to potential misunderstandings or misinterpretations of the code documentation.

## Cause (The cause of the issue):
The cause of the issue is likely a simple oversight or error in the code documentation process, where the `//!` marker was not applied to certain lines that were intended to be comments.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
The solution involved reviewing the affected lines of code (line 36 to line 44) and ensuring that the missing `//!` comment markers were added to the appropriate lines. This step corrected the documentation inconsistency and ensured that all comments were properly marked, as acknowledged in the second comment indicating the issue was fixed.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/56)


# [Title] Missing braces

## Problem Phenomenon (The issue):
The code at lines 520 and 521 of the `socket.c` file in the `ioLibrary_Driver` generates a compiler warning for missing braces. The warning is likely due to a lack of clarity in the intended precedence of operations in the condition expressions.

## Cause (The cause of the issue):
The issue is caused by the absence of explicit braces in the condition expressions, which can lead to confusion about the order of operations. Specifically, the intention to perform a bitwise AND operation before a logical comparison is not clearly expressed, leading to the compiler warning.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
To resolve the compiler warning, ensure that the bitwise AND operation is clearly performed before the logical comparison by adding explicit braces to the condition expressions. The revised code should look like this:

```c
if ((taddr == 0) && ((getSn_MR(sn) & Sn_MR_MACRAW) != Sn_MR_MACRAW)) return SOCKERR_IPINVALID;
if ((port == 0) && ((getSn_MR(sn) & Sn_MR_MACRAW) != Sn_MR_MACRAW)) return SOCKERR_PORTZERO;
```

By adding braces, the intended operation precedence is clarified, eliminating the compiler warning.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/55)


# [Title] -Wsizeof-pointer-memaccess memset(pdhdr, 0, sizeof(pdhdr));

## Problem Phenomenon (The issue):
When compiling the code, a warning is generated due to the improper use of `sizeof` in the `memset` function. The warning indicates that the argument to `sizeof` in the `memset` call is the same expression as the destination, suggesting that it should be dereferenced.

## Cause (The cause of the issue):
The cause of the issue is the use of `sizeof(pdhdr)` in the `memset` function, where `pdhdr` is a pointer. The `sizeof` operator is returning the size of the pointer itself rather than the size of the data structure it points to. This is causing the warning because the `memset` function is not being provided with the correct size of the memory block to set.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
To resolve the warning, the `pdhdr` pointer needs to be dereferenced within the `sizeof` operator to ensure that the `memset` function receives the correct size of the data structure being pointed to. The solution involves changing the code from:

```c
memset(pdhdr, 0, sizeof(pdhdr));
```

to:

```c
memset(pdhdr, 0, sizeof(*pdhdr));
```

This change ensures that the `sizeof` operator returns the size of the object pointed to by `pdhdr`, rather than the size of the pointer itself, thereby resolving the warning.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/54)


# [Title] problem about httpserver 

## Problem Phenomenon (The issue):
When making requests to the HTTP server using the provided code, the first request succeeds and returns the correct response. However, subsequent requests either return blank responses or produce corrupted/garbled outputs.

## Cause (The cause of the issue):
The issue is caused by the `file_offset` not being reset correctly after the data has been sent. This results in the offset pointing to an incorrect address during subsequent requests, leading to blank or corrupted responses.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
The problem can be resolved by ensuring that the `flag_datasend_end` is set to `1` correctly when all data has been sent. Specifically, in the `send_http_response_body` function, ensure that `flag_datasend_end` is set to `1` when `send_len` is less than or equal to `DATA_BUF_SIZE - 1`. This will trigger the resetting of the `file_offset`, `file_start`, and `file_len` in the `HTTPSock_Status` structure:

1. Verify that in the `send_http_response_body` function, after determining the `send_len`, you check if `send_len` is less than or equal to `DATA_BUF_SIZE - 1`.
2. If true, set `flag_datasend_end` to `1` to ensure the `file_offset` is reset for the next request.
3. This will allow the server to correctly process and respond to subsequent requests.

By implementing these changes, the HTTP server should handle multiple requests correctly without returning blank or corrupted responses.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/50)


# [Title] Adding support for C++ (calling C functions)

## Problem Phenomenon (The issue):
Lack of C++ support in the current implementation of `.h` files, which requires conditional compilation to ensure compatibility with both C and C++.

## Cause (The cause of the issue):
The existing `.h` files do not include conditional compilation directives that allow the code to be compiled with a C++ compiler, which is necessary for ensuring compatibility and proper linking of C functions when used in C++ projects.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
Add the following conditional compilation directives to the `.h` files to support C++:

```c
#ifdef __cplusplus
extern "C" {
#endif

// C prototypes

#ifdef __cplusplus
}
#endif
```

These changes should be added at the beginning and the end of the function prototypes in the `.h` files to ensure that C++ compilers treat the enclosed code as C, thus enabling proper linkage and compatibility.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/49)


# [Title] DHCP client stops working sometimes

## Problem Phenomenon (The issue):
The DHCP client stops working intermittently. The program remains in a waiting state if the socket is closed, as indicated by the line of code in `socket.c`, line 193: `while(getSn_SR(sn) == SOCK_CLOSED);`. This issue occurs even when the ethernet cable is continuously connected.

## Cause (The cause of the issue):
The issue is suspected to be related to hardware connection instability. The user is utilizing a W5500 ethernet controller with an NRF52832 microprocessor. The connection via cables is unstable, leading to the W5500 resetting itself periodically, clearing all data such as IP, mask, gateway, MAC address, etc., to zero.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
1. Refer to the BLE Board created by WIZnet for guidance:
   - [WIZnet BLE to Ethernet Wiki](https://wizwiki.net/wiki/doku.php?id=oshw_using_wiznet:bletoethernet)

2. Review and implement the reference schematic for the NRF52832 and W5500 to ensure proper hardware connections:
   - [Reference Schematic](https://drive.google.com/open?id=0Bx-BD_H8XJXxVWdrcVliY1E1RGM)

3. Utilize the example firmware for NRF52832 and W5500 to verify and improve stability:
   - [Example Firmware on GitHub](https://github.com/Wiznet/WIZBLE510_ETHERNET)

By reviewing and adopting the above resources and examples, the hardware connection issues might be mitigated, thereby resolving the problem with the DHCP client.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/48)


# [Title] fix getsockopt() SO_REMAINSIZE then set SF_TCP_NODELAY

## Problem Phenomenon (The issue):
The function `getsockopt()` returns an incorrect result for `SO_REMAINSIZE` when the socket flag is set to `Sn_MR_TCP` and `SF_TCP_NODELAY`.

## Cause (The cause of the issue):
The condition in the `getsockopt()` function checks for equality (`==`) with `Sn_MR_TCP`, which causes it to fail when additional flags like `SF_TCP_NODELAY` are present. This leads to the incorrect handling of the socket mode, resulting in an inaccurate `SO_REMAINSIZE` value.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
Modify the condition in the `getsockopt()` function to use a bitwise AND operation (`&`) instead of an equality check (`==`). This allows the function to correctly identify the presence of the `Sn_MR_TCP` flag even when other flags are set.

### Code Change:
```c
- if(getSn_MR(sn) == Sn_MR_TCP)
+ if(getSn_MR(sn) & Sn_MR_TCP)
    *(uint16_t*)arg = getSn_RX_RSR(sn);
```

This change ensures that the correct value for `SO_REMAINSIZE` is returned when the socket is in TCP mode, even if additional flags are present.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/47)


# [Title] Fix in DNS client

## Problem Phenomenon (The issue):
The variables "retry_count" and "dns_1s_tick" are not being reset to zero each time the `DNS_init` function is called. This could lead to incorrect DNS processing behavior because old values may persist across DNS initialization calls.

## Cause (The cause of the issue):
The variables "retry_count" and "dns_1s_tick" are not initialized properly within the `DNS_init` function, causing them to retain previous states instead of starting from zero with each new DNS initialization.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
To solve the issue, the following code changes should be made to ensure that "retry_count" and "dns_1s_tick" are reset to zero within the `DNS_init` function:

1. Add the following lines in the `DNS_init` function to reset the variables:
   ```c
   retry_count = 0;
   dns_1s_tick = 0;
   ```

2. Modify the `dns.c` file as follows, based on the provided diff:
   ```diff
   diff --git a/Internet/DNS/dns.c b/Internet/DNS/dns.c
   index d4e5806..b412fc2 100644
   --- a/Internet/DNS/dns.c
   +++ b/Internet/DNS/dns.c
   @@ -120,6 +120,7 @@ uint8_t  DNS_SOCKET;    // SOCKET number for DNS
    uint16_t DNS_MSGID;     // DNS message ID
    
    uint32_t dns_1s_tick;   // for timout of DNS processing
   +static uint8_t retry_count;
    
    /* converts uint16_t from network buffer to a host byte order integer. */
    uint16_t get16(uint8_t * s)
   @@ -472,7 +473,6 @@ int16_t dns_makequery(uint16_t op, char * name, uint8_t * buf, uint16_t len)
    
    int8_t check_DNS_timeout(void)
    {
   -	static uint8_t retry_count;
    
    	if(dns_1s_tick >= DNS_WAIT_TIME)
    	{
   @@ -496,6 +496,8 @@ void DNS_init(uint8_t s, uint8_t * buf)
    	DNS_SOCKET = s

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/46)


# [Title] IP Address set two times 

## Problem Phenomenon (The issue):
There are two calls to `setSIPR(zeroip);` in `dhcp.c` at lines 915 and 916, which appear to be a mistake.

## Cause (The cause of the issue):
The issue is likely caused by an erroneous repetition of the `setSIPR(zeroip);` function call, which may not have been intended in the code.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
The solution involves correcting the mistake by removing the redundant call to `setSIPR(zeroip);` in the `dhcp.c` file. Only one call should be present if necessary, ensuring the code functions as intended without the redundancy.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/45)


# [Title] _WIZCHIP_ < W5200 : wizchip_init : Infinite loop when buffer size is set to 0

## Problem Phenomenon (The issue):
An infinite loop occurs when there is a socket buffer set with a zero size in the `wizchip_conf.c` file of the ioLibrary_Driver.

## Cause (The cause of the issue):
The infinite loop is caused by the logic in the code where the buffer size is set to zero, which leads to the condition in the while loop never being met, thus creating an infinite loop.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
Modify the while loop conditions in the `wizchip_conf.c` file to include a check for a zero buffer size, preventing the infinite loop. The changes are as follows:

```c
while((txsize[i] >> j != 1) && (txsize[i] != 0)){j++;}
while((rxsize[i] >> j != 1) && (rxsize[i] != 0)){j++;}
```

This change ensures that if the buffer size is zero, the loop will not continue indefinitely, thus preventing the infinite loop.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/44)


# [Title] MQTT

## Problem Phenomenon (The issue):

1. The function `w5x00_write()` in `mqtt_interface.c` is declared with three arguments but is incorrectly assigned to a pointer `mqttwrite` that is expected to take four arguments. This causes a mismatch in function pointer assignment.
2. Similarly, the `w5x00_read()` function in `mqtt_interface.c` has a similar issue with argument mismatch.
3. In `mqtt_interface.c`, line 165, the variable `myport` is declared as `uint8_t` but should be `uint16_t` to avoid truncation of the integer value.

## Cause (The cause of the issue):

- The declaration of the `w5x00_write()` and `w5x00_read()` functions does not match the expected function pointer signature used in the MQTT client, leading to assignment from incompatible pointer types.
- The variable `myport` is declared with an incorrect data type (`uint8_t` instead of `uint16_t`), which results in an implicit truncation of larger integer values.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):

1. **Function Signature Correction:**
   - Ensure that the `w5x00_write()` function is defined with four arguments to match the expected function pointer signature used in `MQTTClient.c`.
   - Similarly, adjust the `w5x00_read()` function to match the expected signature.

2. **Variable Declaration Correction:**
   - Change the declaration of `myport` from `uint8_t myport = 12345;` to `uint16_t myport = 12345;` to prevent integer truncation.

3. **Code Example for Changes:**
   - Update the `w5x00_write()` and `w5x00_read()` function definitions to include the correct number of arguments.
   - For `myport`, update the line in `mqtt_interface.c` as follows:
     ```c
     uint16_t myport = 12345;
     ```

4. **Testing:**
   - After making these changes, compile the code and test the MQTT functionality to ensure that the bugs are resolved and the program behaves as expected.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/43)


# [Title] Macro name error creating infinite loop

## Problem Phenomenon (The issue):
The code in `wizchip_conf.c` contains a preprocessor condition that always evaluates to true, causing the execution of code that results in an infinite loop when compiled for the W5500 chip.

## Cause (The cause of the issue):
The issue is caused by a typo in the preprocessor condition on lines 442 and 476 of `wizchip_conf.c`. The condition uses `#if __WIZCHIP_ < W5200`. The identifier `__WIZCHIP_` does not exist, so its value defaults to 0, causing the condition to always be true. The correct identifier is `_WIZCHIP_` (with only one underscore).

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
1. Open the `wizchip_conf.c` file.
2. Locate lines 442 and 476 where the preprocessor condition is defined.
3. Change `#if __WIZCHIP_ < W5200` to `#if _WIZCHIP_ < W5200` by removing one underscore.
4. Save the changes to the file.
5. Recompile the code to ensure that the condition now evaluates correctly and does not cause an infinite loop for the W5500 chip.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/39)


# [Title] Ethernet/socket.c:520:36: error: suggest parentheses around comparison in operand of '&' [-Werror=parentheses]

## Problem Phenomenon (The issue):
The file `Ethernet/socket.c` cannot be built with the `-Werror` flag due to errors suggesting the need for parentheses around comparisons in the operand of `&`. These errors occur at lines 520 and 521 in the `sendto` function and are treated as errors because all warnings are being treated as errors.

## Cause (The cause of the issue):
The issue is caused by the lack of parentheses around the comparison in the operand of the `&` operator within the conditional statements in the `sendto` function. This causes the compiler to warn about potential precedence issues, which are elevated to errors due to the `-Werror` flag.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
To resolve the issue, add parentheses around the comparisons to clarify the intended logic and satisfy the compiler's requirements. Modify the conditional statements as follows:

```c
if ((taddr == 0) && ((getSn_MR(sn) & Sn_MR_MACRAW) != Sn_MR_MACRAW)) return SOCKERR_IPINVALID;
if ((port == 0) && ((getSn_MR(sn) & Sn_MR_MACRAW) != Sn_MR_MACRAW)) return SOCKERR_PORTZERO;
```

These changes ensure that the comparisons are correctly interpreted by the compiler, resolving the warnings and allowing the code to be built successfully with the `-Werror` flag enabled.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/38)


# [Title] Ethernet/wizchip_conf.c:837:10: error: unused variable 'k' [-Werror=unused-variable]

## Problem Phenomenon (The issue):
When attempting to build the file `Ethernet/wizchip_conf.c` with the `-Werror` flag enabled, the build process fails due to unused variables in the `wizchip_setnetinfo` function. Specifically, the variables `i`, `j`, and `k` are declared but not used, resulting in errors with the `-Werror=unused-variable` flag.

## Cause (The cause of the issue):
The issue is caused by declaring variables `i`, `j`, and `k` within the `wizchip_setnetinfo` function that are not utilized in the function's logic. The `-Werror` flag treats these warnings as errors, preventing successful compilation.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
1. **Code Change**: Remove or comment out the unused variables `i`, `j`, and `k` in the `wizchip_setnetinfo` function within the `Ethernet/wizchip_conf.c` file if they are not necessary for any future implementation.
   ```c
   // Original line causing the error
   int i, j, k;

   // Modified line after removing unused variables
   // int i, j, k;
   ```
2. **Alternative Approach**: If the variables are intended for future use, consider temporarily commenting them out or using them in a way that satisfies the compiler without causing warnings.
3. **Pull Request Reference**: Check pull request #53 for a potential fix or reference to the issue being resolved.
4. **Build Configuration**: If removal of the variables is not feasible, consider compiling without the `-Werror` flag for development purposes, but this should be avoided in production to maintain code quality.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/37)


# [Title] Ethernet/wizchip_conf.c:166:7: error: missing braces around initializer [-Werror=missing-braces]

## Problem Phenomenon (The issue):
The project cannot be built with the `-Werror` flag enabled. Errors occur due to missing braces around initializers and suggest parentheses around comparisons in operands.

## Cause (The cause of the issue):
The issue arises from using the `-Werror` flag, which treats warnings as errors. The code contains warnings related to missing braces around initializers and the need for parentheses around comparisons in operands, which are turned into errors due to the `-Werror` flag.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
To fix the compile warnings and allow the project to build successfully with `-Werror`, the following code modifications were made:

```c
_WIZCHIP  WIZCHIP =
{
    _WIZCHIP_IO_MODE_,
    _WIZCHIP_ID_,
    {   //WIZCHIP.CRIS
        wizchip_cris_enter,
        wizchip_cris_exit
    },
    {   //WIZCHIP.CS
        wizchip_cs_select,
        wizchip_cs_deselect
    },
    {   //WIZCHIP.IF
        {   //WIZCHIP.IF.BUS
            wizchip_bus_readdata,
            wizchip_bus_writedata
        }
        //Empty SPI element //WIZCHIP.IF.SPI
    },
};
```

This code change involves adding the missing braces around the initializer to resolve the warnings and ensure the code compiles without errors when using `-Werror`.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/36)


# [Title] This comment doesn't make sense

## Problem Phenomenon (The issue):
A specific number in the `dhcp.h` file of the `ioLibrary_Driver` cannot be modified, leading to issues when someone attempts to change it.

## Cause (The cause of the issue):
The number in question, which is related to the DHCP identifier, was initially up to the vendor's discretion but has since been standardized. Changing this number can cause issues because it must adhere to the standard.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
- The comment in the code should be updated to indicate that the DHCP identifier is standardized and should not be changed. A suggested comment is: "DHCP identifier. Do not change."
- Ensure all users are aware of the standardization by updating documentation and code comments to prevent inadvertent modifications.
- The issue will be resolved by updating the comment in the code to reflect its standardized nature, as indicated by the discussion in the comments.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/35)


# [Title] use w5500 find some thing wrong, need help,thanks

## Problem Phenomenon (The issue):
The issue is that the function `wizphy_getphylink()` in the file `wizchip_conf.c` always returns `PHY_LINK_OFF` when using the W5500 chip, regardless of the actual physical link status.

## Cause (The cause of the issue):
The cause of the issue is a missing `else` statement in the conditional logic for the W5500 chip in the `wizphy_getphylink()` function. Without the `else`, the variable `tmp` is set to `PHY_LINK_OFF` immediately after being set to `PHY_LINK_ON`, resulting in the function always returning `PHY_LINK_OFF`.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
To solve the problem, modify the `wizphy_getphylink()` function in `wizchip_conf.c` as follows:

```c
#elif _WIZCHIP_ == W5500
   if(getPHYCFGR() & PHYCFGR_LNK_ON)
      tmp = PHY_LINK_ON;
else
      tmp = PHY_LINK_OFF;
#else
```

By adding the `else` statement, the code correctly sets `tmp` to `PHY_LINK_ON` when the physical link is active, and to `PHY_LINK_OFF` when it is not, accurately reflecting the physical link status.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/33)


# [Title] Type change for variable "any_port" in loopback function.

## Problem Phenomenon (The issue):
The issue involves a type change for the variable "any_port" within the loopback function.

## Cause (The cause of the issue):
The problem likely stemmed from an incorrect or unintended type change for the variable "any_port", which may have caused unexpected behavior in the loopback function.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
The issue was resolved, as indicated by the comment "Case closed". However, specific details on the code changes, configuration adjustments, or actions taken to solve the problem were not provided in the issue content.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/32)


# [Title] flush udp buffer

## Problem Phenomenon (The issue):
The user is unable to find a function in the library to flush/clear/refresh the UDP socket buffer while using a W5500 to communicate with a real-time controller. Regular flushing of the buffer is necessary for their application.

## Cause (The cause of the issue):
The issue arises from the user's inability to locate the function within the library documentation or codebase that facilitates flushing the socket buffer for the W5500.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
For the W5500, W5100, and W5200, the socket buffer can be flushed by updating `Sn_RX_RD` without data copy and commanding with `Sn_CR[RECV]`. Below is a sample function to flush the data of the socket buffer:

```c
int_t sock_flush(uint8_t s) {
    int_t ret = 0;
    if(getSn_SR(s) == SOCK_CLOSED) return -1;
    ret = getSn_RX_RSR(s);
    setSn_RX_RD(s, (getSn_RX_RD(s) + ret));
    return ret;
}
```

Note: For the W5300, flushing the socket data is not possible. For UDP and IPRAW sockets, reopen the socket to flush data. There is no flush method available for TCP sockets.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/31)


# [Title] How to compile w5500 driver for android.

## Problem Phenomenon (The issue):
The user wants to compile the W5500 driver for Android but cannot find it in the kernel driver path where other similar drivers, like the W5300, are located.

## Cause (The cause of the issue):
The user is likely using an Android kernel version that does not include the W5500 driver, which was added to the official Linux kernel starting from version 4.7.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
1. Verify the Android kernel version being used:
   - If it is version 4.7 or higher, the W5500 driver should be supported.
   - If it is a version lower than 4.7, the kernel will need to be updated to at least version 4.7 to include support for the W5500 driver.

2. Reference the Linux kernel commit history for additional context on the W5500 driver support:
   - Visit the [Linux kernel commit history: support W5500](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=35ef7d689d7d54ab345b179e50c749fe3a2529eb) for detailed information on the specific commit that added support for the W5500 driver.

3. If the driver is supported in the kernel version, ensure the appropriate configuration is enabled to compile the driver. This might involve setting the correct configuration options in the kernel build system to include the W5500 driver.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/26)


# [Title] Potentially incorrect Host Name during DHCP

## Problem Phenomenon (The issue):
The DHCP host name is constructed by appending the last three bytes of the MAC address to a constant `HOST_NAME`. If any of these bytes are smaller than 0x20, it causes issues with certain routers (e.g., Zyxel Keenetic Omni II), which may stop displaying the DHCP clients list page.

## Cause (The cause of the issue):
The issue arises because the code directly appends the last three bytes of the MAC address to the host name without ensuring that they are in a displayable format. Bytes smaller than 0x20 can interfere with the display functionality of some routers.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
1. Modify the code to convert each byte of the MAC address to a hexadecimal string representation before appending it to the host name.
2. Add a helper function `NibbleToHex()` to facilitate this conversion.
   
The revised code for constructing the DHCP host name is as follows:
```c
// host name
pDHCPMSG->OPT[k++] = hostName;
pDHCPMSG->OPT[k++] = 0;          // fill zero length of hostname
for(i = 0 ; HOST_NAME[i] != 0; i++)
    pDHCPMSG->OPT[k++] = HOST_NAME[i];
pDHCPMSG->OPT[k++] = NibbleToHex(DHCP_CHADDR[3] >> 4); 
pDHCPMSG->OPT[k++] = NibbleToHex(DHCP_CHADDR[3]);
pDHCPMSG->OPT[k++] = NibbleToHex(DHCP_CHADDR[4] >> 4); 
pDHCPMSG->OPT[k++] = NibbleToHex(DHCP_CHADDR[4]);
pDHCPMSG->OPT[k++] = NibbleToHex(DHCP_CHADDR[5] >> 4); 
pDHCPMSG->OPT[k++] = NibbleToHex(DHCP_CHADDR[5]);
pDHCPMSG->OPT[k - (i+6+1)] = i+6; // length of hostname
```

Add the following helper function `NibbleToHex()`:
```c
char NibbleToHex(uint8_t nibble)
{
  nibble &= 0x0F;
  if (nibble <= 9)
    return nibble +

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/23)


# [Title] Use of Malloc

## Problem Phenomenon (The issue):
The `httpServer.c` file in the `ioLibrary_Driver` project uses `malloc` to store strings, which is problematic for smaller embedded targets like AVR microcontrollers. The user is seeking a way to eliminate the use of `malloc` in favor of a fixed-length string buffer or an alternative, such as a `#define`.

## Cause (The cause of the issue):
The use of dynamic memory allocation (`malloc`) in the `httpServer.c` file is not ideal for smaller embedded systems due to limited memory resources and potential fragmentation issues.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
1. Replace the `malloc` calls in `httpServer.c` with fixed-length string buffers. This involves identifying all instances of `malloc` and switching to statically allocated arrays with a predefined size.
2. Alternatively, introduce a preprocessor directive (`#define`) that allows users to choose between dynamic and static allocation. This provides flexibility for different target environments.
3. For reference and guidance, examine the `httpServer` implementation in the WIZ550web project, as it reportedly does not use `malloc`.
4. Review the source code and project structure in both the `ioLibrary_Driver` and `WIZ550web_App` projects to ensure consistency and eliminate redundant code where possible.
5. Consult the WIZ550web documentation and resources for additional implementation details and best practices.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/22)


# [Title] syntax error

## Problem Phenomenon (The issue):
Syntax error in the code.

## Cause (The cause of the issue):
A misplaced or unnecessary ')' character that should be removed.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
Remove the ')' character from the specified location in the code:  
https://github.com/Wiznet/ioLibrary_Driver/blob/069a81350e8ea0da2d210ab01db97895bba20399/Ethernet/W5300/w5300.h#L1338

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/21)


# [Title] HTTP POST & Get

## Problem Phenomenon (The issue):
A user is seeking guidance on how to create HTTP POST and GET messages to a server using the Wiznet5100 and is unsure how to start using the included HTTP library.

## Cause (The cause of the issue):
The user lacks the necessary information or resources to implement HTTP communication using the Wiznet5100 and is seeking assistance to understand how to use the HTTP library for their specific use case.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
1. It is suggested to seek advice on the Wiznet forum, which is likely a more appropriate platform for discussing such specific use cases: [forum.wiznet.io](url).
2. Review the provided links for examples of similar implementations using STM32F103 and W5500, which might offer insights:
   - [WIZ550web GitHub Repository](https://github.com/Wiznet/WIZ550web)
   - [WIZ550Web_STM32F103RB_CoIDE GitHub Repository](https://github.com/Wiznet/WIZ550Web_STM32F103RB_CoIDE)

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/20)


# [Title] w550io + nrf51(pca10028) : Network initialization succeeds until first restart of host after it has been freshly flashed(programmed)

## Problem Phenomenon (The issue):
The network initialization on an nrf51 board with added Ethernet capability succeeds when the board is recently programmed but fails upon restarting the board. However, if the board is reprogrammed with the same .hex file, the network initialization is successful again.

## Cause (The cause of the issue):
The problem appears to be related to the persistence of the network initialization state. It is likely that crucial initialization parameters or states are not being retained or properly re-initialized after a restart, but are correctly set during the programming process.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
1. Ensure that the network initialization code is designed to run both at initial programming and on every restart.
2. Verify that all necessary hardware registers and configurations are re-initialized after a restart.
3. Check for any dependencies in the initialization sequence that might be affected by a restart.
4. Consider adding non-volatile storage mechanisms if there are parameters that need to be retained across restarts.
5. Test the initialization sequence in a debugger to ensure that all steps are executed correctly on a restart.
6. Review and ensure that the firmware correctly handles resets and power cycles, especially any startup configurations.
7. Engage with online forums such as [forum.wiznet.io](url) for community support and advice specific to your hardware setup.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/19)


# [Title] W5500 : Is not consistently able to assign GW, SUBM, IP, & MAC

## Problem Phenomenon (The issue):
The user is attempting to set up a connection between an NRF51 and a Wiznet board using the ioLibrary_Driver. The setup is inconsistent, with the W5500 sometimes failing to initialize, resulting in failure to assign IP, MAC, gateway, and subnet mask, although DNS always initializes successfully. The issue frequency is high, with a success to failure ratio of 1:50.

## Cause (The cause of the issue):
The root cause of the issue is the incorrect SPI mode configuration. The Wiznet 5100 only supports SPI mode 0, but the library being used initializes the SPI interface in mode 3, causing the inconsistency. When the device is restarted, the network initialization fails unless the host is re-flashed, indicating a potential issue with retaining configuration settings across resets.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
1. Change the SPI mode configuration to ensure compatibility with the Wiznet 5100:
   - Modify the SPI initialization code to set the mode to SPI_MODE0. Here is a code snippet for the correct configuration:
     ```c
     void spi0_master_init()
     {
         SPIConfig_t spi_info = {.Config.Fields.BitOrder = SPI_BITORDER_MSB_LSB,
                                 .Config.Fields.Mode     = SPI_MODE0,
                                 .Frequency              = SPI_FREQ_8MBPS,
                                 .Pin_SCK                = ARDUINO_13_PIN,
                                 .Pin_MOSI               = ARDUINO_11_PIN,
                                 .Pin_MISO               = ARDUINO_12_PIN,
                                 .Pin_CSN                = ARDUINO_10_PIN};	
         spi_master_init(SPI0, &spi_info);
     }
     ```
2. Verify the hardware connections and ensure they match the reference schematic provided in the related guides.
3. If using a different chip like the Wiznet 5500, ensure it also supports the chosen SPI mode.
4. For persistent network initialization across restarts, investigate the firmware settings to ensure they are retained without needing to re-flash the device.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/18)


# [Title] Network_init(); not setting the Mac, IP, Subnet , Gw, DNS

## Problem Phenomenon (The issue):
The `network_init()` function does not consistently assign the MAC, IP, subnet (SUBM), and gateway (GW) addresses when using a specific library, while the DNS address is set successfully. This inconsistency leads to the other network parameters returning as 0.0.0.0.

## Cause (The cause of the issue):
The root cause appears to be an issue with the interface between the host and the W5100 chip, particularly when using SPI or Bus interfaces. The problem may be related to either setting or getting network information using `ctlnetwork(CN_SET_NETINFO, ...)` and `ctlnetwork(CN_GET_NETINFO, ...)`, as the DNS is the only parameter consistently set correctly.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
1. **Verify Interface Connections**: Ensure that the connections between the host (e.g., NRF51) and the Wiznet board are correct as per the setup guide (e.g., the link provided: http://wiznetmuseum.com/portfolio-items/ble-to-ethernet-thin-gateway/).

2. **Check Interface Type**: Confirm whether you are using SPI or Bus and ensure that the interface is correctly configured and operational.

3. **Use Diagnostic Tools**: Utilize tools like a logic analyzer to verify the output and diagnose the communication between the host and the W5100 chip.

4. **Consult Wiznet Resources**: Visit [forum.wiznet.io](url) for additional support and possible solutions from the community or the Wiznet support team. Consider sharing your schematic or gerber files to support@wiznet.io for further hardware verification.

5. **Collaborate with Peers**: Consider exchanging contact information with others facing the same issue to share findings and solutions.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/17)


# [Title] Define what chip is used TODO

## Problem Phenomenon (The issue):
The user is unable to open the Doxygen document for the ioLibrary related to the Wiznet 5100 chip. As a result, they are unsure about the necessary configuration changes needed for the program to recognize the chip as a W5100.

## Cause (The cause of the issue):
The issue arises because the Doxygen document, which provides guidance on defining the chip and host interface mode in `wizchip_conf.h`, is not accessible to the user. This lack of access leaves the user unsure about how to configure the program correctly for the W5100 chip.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
1. Locate the correct version of the Doxygen document within the library. This document should provide detailed instructions on configuring `wizchip_conf.h`.
2. Review the document to identify the necessary changes required to define the W5100 chip and the host interface mode.
3. Implement the changes as per the instructions in the document:
   - Define the W5100 chip in `wizchip_conf.h`.
   - Specify the appropriate host interface mode in the same configuration file.
4. Save the changes and ensure that the program recognizes the W5100 chip configuration, as intended.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/16)


# [Title] Indentation

## Problem Phenomenon (The issue):
The project contains a mixture of spaces and tabs for indentation and lacks a .editorconfig file. This inconsistency makes the source code difficult to read both in an editor and on the GitHub website.

## Cause (The cause of the issue):
The absence of a .editorconfig file and inconsistent use of spaces and tabs for indentation in the source code leads to readability issues.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
To address this issue, create a .editorconfig file with the following configuration:
```ini
# editorconfig.org

root = true

[*]
charset = utf-8
end_of_line = lf
indent_size = 3
indent_style = tab
insert_final_newline = true
trim_trailing_whitespace = true
```
This configuration ensures consistent use of tabs for indentation, sets the character set to UTF-8, uses LF for end-of-line characters, and enforces other formatting standards to improve code readability.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/15)


# [Title] bug , DHCP fill the  length of HOST_NAME

## Problem Phenomenon (The issue):
The hostname length in the DHCP message is being incorrectly calculated due to the addition of three extra bytes from the MAC address. This results in the hostname not being parsed correctly by routers.

## Cause (The cause of the issue):
The issue arises from the way the length of the hostname is calculated in the `dhcp.c` file. The calculation mistakenly includes three additional bytes from the MAC address, which are intended as a delimiter. This causes the actual length of the hostname to be misrepresented.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
Review and modify the section of the `dhcp.c` file where the hostname length is calculated. Ensure that the length calculation does not include the three extra MAC address bytes unless they are explicitly intended to be part of the hostname. This may involve adjusting the logic around the `OPT` array manipulation:

1. Locate the following code in the `dhcp.c` file:
   ```c
   pDHCPMSG->OPT[k++] = DHCP_CHADDR[3];
   pDHCPMSG->OPT[k++] = DHCP_CHADDR[4];
   pDHCPMSG->OPT[k++] = DHCP_CHADDR[5];
   pDHCPMSG->OPT[k - (i+3+1)] = i+3; // length of hostname
   ```

2. Assess whether the additional bytes from `DHCP_CHADDR` are necessary for your application. If not, remove or adjust this part of the code to accurately reflect the true length of the hostname without the extra bytes.

3. Test the modified code to ensure that routers can correctly parse the hostname without errors.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/14)


# [Title] ioLibrary Licensing 

## Problem Phenomenon (The issue):
There is no License.txt file in the project, leading to uncertainty about the licensing terms and whether the project can be used commercially without any fees.

## Cause (The cause of the issue):
The project repository does not contain a License.txt file, which typically specifies the licensing terms under which the project code can be used, modified, or distributed.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
1. Determine the desired license for the project. Common open-source licenses include MIT, Apache 2.0, GPL, etc.
2. Create a License.txt file in the root directory of the project.
3. Add the text of the chosen license to the License.txt file. Many licenses have standard text available online.
4. Commit the License.txt file to the repository to ensure it is visible to all users.
5. Update the project's README or documentation to clearly state the licensing terms.
6. If commercial use is allowed, specify any conditions or fees associated with such use in the License.txt or accompanying documentation.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/13)


# [Title] getsockopt SO_PACKINFO has incorrect socket mode check

## Problem Phenomenon (The issue):
The getsockopt() function at socket.c:905 is incorrectly using the CHECK_SOCKMODE() macro to verify that the socket is a TCP socket when attempting to use the SO_PACKINFO option. This results in the inability to use the SO_PACKINFO option for UDP and MACRAW sockets, which should also support this flag.

## Cause (The cause of the issue):
The issue is caused by the misuse of the CHECK_SOCKMODE() macro, which is currently set to verify only TCP sockets for the SO_PACKINFO option. This macro does not account for the validity of the SO_PACKINFO option for UDP and MACRAW sockets.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
Modify the CHECK_SOCKMODE() macro or the surrounding logic at socket.c:905 to accommodate UDP and MACRAW sockets in addition to TCP sockets when using the SO_PACKINFO option. This may involve updating the macro definition or implementing additional checks to ensure that the SO_PACKINFO option is appropriately validated for all applicable socket types (TCP, UDP, and MACRAW).

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/12)


# [Title] w5500 lib for ESP

## Problem Phenomenon (The issue):
The user is interested in modifying the Ethernet (w5500) library to run on the ESP8266 platform.

## Cause (The cause of the issue):
The issue arises from the need to adapt the w5500 Ethernet library, which may not natively support the ESP8266, requiring modification to ensure compatibility, particularly with the SPI pin configuration.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
1. Verify that the ESP8266 has an available SPI pin configuration to support the w5500 Ethernet module.
2. Refer to the commit mentioned in the issue for guidance on changes needed to support SPI communication on ESP8266: [ESP8266 Arduino commit](https://github.com/esp8266/Arduino/commit/2a01c2ad531b2a71983a729a00ca9bf8caa1b3fa).
3. Attempt to modify the Ethernet library code to utilize the available SPI pins on the ESP8266.
4. Test the modified library to ensure that it allows the ESP8266 to communicate effectively with the Ethernet (w5500) module.
5. Troubleshoot any communication issues by reviewing SPI settings and ensuring that the pin assignments are correctly configured.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/11)


# [Title] NTP_SOCKET is not initialized

## Problem Phenomenon (The issue):
In `sntp.c`, the `NTP_SOCKET` is not being initialized in the `SNTP_init` function, which may lead to issues in the SNTP functionality.

## Cause (The cause of the issue):
The lack of initialization for `NTP_SOCKET` in the `SNTP_init` function is the root cause of the problem.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
Refer to commit `0cabf53` in the repository and examine the NTP example project available at:
https://github.com/Wiznet/SNTP_LPC11E36_LPCXpresso
This commit and example project include the necessary changes and configurations to correctly initialize `NTP_SOCKET` in the `SNTP_init` function.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/9)


# [Title] Multibyte transactions with w5100

## Problem Phenomenon (The issue):
The user encountered an issue while integrating a library into an AVR weather station project, specifically struggling to initialize the W5100 such that it responds to ping.

## Cause (The cause of the issue):
The issue was caused by a change in version 3.0 of the library, where the chip select and deselect calls were incorrectly moved out of the loop in the `WIZCHIP_WRITE_BUF` and `WIZCHIP_READ_BUF` functions. This change did not align with the W5100's requirement for chip select control on every byte transaction, as the W5100 does not support multi-byte transactions like the W5200 and later models.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
The solution involved reverting the chip select and deselect calls back into the loop within the `WIZCHIP_WRITE_BUF` and `WIZCHIP_READ_BUF` functions, ensuring that the chip gets selected and deselected on every transaction. This change was implemented in an updated version of the library (V3.0.1), which resolved the issue for the user.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/7)


# [Title] Code compatibility problem W5500 <-> W5200 and some more warnings

## Problem Phenomenon (The issue):
The code is running fine with the W5500 chip, but when switching to the W5200 chip by changing the `_WIZCHIP_` define in `wizchip_conf.h`, the code compiles without errors but does not function correctly. Specifically, the issue is with setting the socket interrupt mask register (SIMR) for socket 0 interrupts, where the current implementation incorrectly points `setSIMR()` to `setIMR2()` instead of `setIMR()`.

## Cause (The cause of the issue):
The problem arises from incorrect mapping of functions between the W5500 and W5200 chips. The mappings for interrupt registers are incorrect:
- `setSIMR()` should point to `setIMR()`, not `setIMR2()`.
- The compatibility issue arises because `setIMR()` and `getIMR()` were set to handle IMR2, and `setIMR2()` and `getIMR2()` were set to handle _IMR_ with a mask of `& 0xA0`, which is incorrect for the intended functionality.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
1. Modify the code so that `setSIMR()` and `getSIMR()` point to `setIMR()` and `getIMR()` respectively, to ensure they handle the _IMR_ register correctly.
2. Update `setIMR2()` and `getIMR2()` to manage the IMR2 register.
3. Remove the "& 0xA0" mask from `setIMR2()` and `getIMR2()` to ensure compatibility and correct functionality.
4. Test the code by setting the SIMR (socket interrupt mask register) to activate the interrupt for a specific socket and verify the value after writing to confirm the correct behavior.
   - For example, for socket 1 interrupt:
     ```c
     setSIMR(0x02); // activate interrupt for socket 1
     simr = getSIMR(); // check value after write
     ```
   - Ensure the behavior is consistent for both W5500 and W5200 without changes to the main application logic.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/4)


# [Title] Integer conversion warning

## Problem Phenomenon (The issue):
A warning is generated by the TI compiler in the `socket.c` file at line 436, specifically "#69-D integer conversion resulted in a change of sign." This warning indicates a potential bug where a negative value (`SOCKERR_TIMEOUT`, which is -13) is being assigned to a variable (`len`) of type `uint16_t`.

## Cause (The cause of the issue):
The issue is caused by an incorrect type assignment. A negative value (`SOCKERR_TIMEOUT`) is being assigned to a variable of type `uint16_t`, which is an unsigned integer type, resulting in a warning and potential unintended behavior.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
The issue was resolved by the repository maintainers, although the specific code changes or configuration updates were not detailed in the issue comments. To resolve such an issue, you would typically ensure that the variable `len` is of a signed integer type that can accommodate negative values, such as `int16_t` or `int32_t`, to avoid any change of sign during assignment.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/3)


# [Title] There is a bug in connect function.

## Problem Phenomenon (The issue):
The "connect()" function was using the wrong array index, causing a bug.

## Cause (The cause of the issue):
The root cause of the issue was an incorrect array index being used within the "connect()" function.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
The issue was resolved by fixing the array index used in the "connect()" function. For detailed changes, please refer to the commit with hash 1cf42721573c786540245aaa30526e3a86dc95dd.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/2)


# [Title] Occur a compile error in LPCXpresso IDE.

## Problem Phenomenon (The issue):
When compiling the code, an error occurs at line 1179 in `w5500.h` stating: "'struct _CRIS' has no member named '__sys_appexit'".

## Cause (The cause of the issue):
The error is caused by an incorrect or missing definition within the `struct _CRIS` in the code, where it attempts to call a non-existent member function `__sys_appexit`.

## Solution (Concrete code changes, configuration changes, step-by-step actions, etc., that actually solved the problem):
The issue was resolved in a previous fix labeled as "Fixed #1". To resolve this issue, review the changes made in the commit linked to "Fixed #1" and apply those changes to ensure that the correct member function is being referenced in the `WIZCHIP_CRITICAL_EXIT()` macro.

[View GitHub Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/1)