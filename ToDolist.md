### Make lib platform independent

- **Suggestion**: Core Feature Request: Ensure compatibility with architectures other than 32-bit little-endian.

Background Explanation: The issue highlights a concern with the current library's reliance on a 32-bit little-endian architecture. This implies that the library may not function correctly on systems with different architectures, such as 64-bit or big-endian systems. Addressing this would involve modifying the library to be architecture-agnostic, ensuring broader compatibility and usability across various hardware platforms. This is important for developers who wish to use WIZnet's solutions on diverse systems without being constrained by architecture-specific limitations.  
- [View Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/155)  


### Convert DNS module into non-blocking

- **Suggestion**: Core Feature Request: Implement a non-blocking version of the DNS_run function to prevent the product from becoming unusable during DNS resolution.

Background Explanation: The current implementation of the DNS_run function in dns.c is blocking for up to 6 seconds, which can render the product unusable during this time. This is a significant issue for users who require continuous operation without interruptions. A non-blocking DNS resolution would allow the system to remain responsive and handle other tasks while waiting for the DNS process to complete. Additionally, handling error values for socket operations like `socket`, `sendto`, and `sendto2` could enable early termination of the DNS_run process, further enhancing performance and reliability. This request implies a need for improved asynchronous processing capabilities within the network solution.  
- [View Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/154)  


### recv() timeout in TCP socket

- **Suggestion**: **Feature Request:**

Implement a method to specify a receive timeout for the `recv()` function in TCP mode, similar to the `setsockopt()` function with the `SO_RCVTIMEO` option available in WinSock and Linux OS. Additionally, support the `SF_IO_NONBLOCK` flag for non-blocking operations during `connect` and `send` functions on the W5500 chip to enable polling mode.

**Background Explanation:**

The request highlights a need for more flexible socket operations in TCP mode on the W5500 chip. Currently, the `recv()` function waits indefinitely for data, which can lead to application hangs if the server does not respond promptly. By allowing a timeout to be set, applications can avoid being stuck in a wait state, improving responsiveness and reliability.

Furthermore, respecting the `SF_IO_NONBLOCK` flag would enable non-blocking operations for `connect` and `send` functions. This would allow applications to continue executing other tasks while waiting for these operations to complete, rather than being stalled. This is particularly important for real-time applications where prolonged blocking can render the product ineffective. Implementing these features would align the W5500's capabilities with those of more widely used network stacks, enhancing its utility in diverse application scenarios.  
- [View Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/149)  


### socket.c out-of-bound write in some architectures.

- **Suggestion**: The core feature request or technical suggestion is:

**Request for Architecture Compatibility:**
The issue highlights a need for architecture compatibility, specifically addressing the problem of storing an IP address in a `uint32_t` variable on architectures where the smallest addressable unit is larger than 8 bits, such as the C2000 architecture. The suggestion is to handle IP addresses as byte arrays and perform bit shifts to ensure correct memory alignment and avoid out-of-bound writes.

**Background Explanation:**
This request implies the need for code that is compatible with different hardware architectures, particularly those with non-standard memory alignment requirements. On some architectures, using a `uint32_t` to store an IP address can lead to incorrect memory access and data corruption due to differences in how memory is addressed. By using byte arrays and bit manipulation, the code can be made more robust and portable across various platforms, preventing issues like overwriting other variables on the stack. This is particularly important for embedded systems and network devices where architecture-specific behavior can lead to critical bugs.  
- [View Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/142)  


### #define IR conflicts with STM32G4 series HAL

- **Suggestion**: The core feature request is the need for namespacing in macros within the Wiznet library to prevent naming conflicts with other libraries or codebases.

**Background Explanation:**
The issue arises from a naming conflict between a macro definition in the Wiznet library and a variable name in the STM32G4xx series microcontroller's code. The macro `#define IR` in the Wiznet library conflicts with a similarly named variable in the STM32 code, leading to build errors. This is a common problem when different codebases use generic names for macros, which can cause unexpected replacements during preprocessing. The suggested solution is to namespace the macros (e.g., `#define WIZ_IR`) to ensure they do not conflict with other code, which is a best practice in library development to enhance compatibility and prevent such issues.  
- [View Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/137)  


### Can the W5500 module directly operate on Ethernet MAC frames and set Network card in Promiscuous mode?

- **Suggestion**: The core feature request is the ability to operate directly on lower-level MAC frames without using the TCP/IP protocol on the W5500 module, similar to how it can be done in Linux using raw sockets and promiscuous mode.

Background Explanation:
The user is attempting to port the Powerlink protocol stack, which requires direct manipulation of MAC frames, bypassing the standard TCP/IP stack. In Linux, this can be achieved using raw sockets and setting the network interface to promiscuous mode. However, the current W5500 API does not seem to support this functionality, as it is primarily designed for TCP/IP operations. The request implies a need for WIZnet to provide a way to access and manipulate raw Ethernet frames directly on their hardware, which would enable the implementation of non-IP-based protocols like Powerlink.  
- [View Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/133)  


### Stuck in while "handshake"

- **Suggestion**: The core feature request or technical suggestion in the GitHub issue is:

**Non-blocking API or Timeout Implementation for recv() Function**

**Background Explanation:**
The user is experiencing a problem where their program gets stuck during the SSL/TLS handshake process because the `recv()` function is blocking indefinitely. The issue arises because the `recvsize` is always zero, and the `getSn_RX_RSR(sn)` function consistently returns zero, indicating that no data is being received. The user is questioning why there is no timeout mechanism to break out of this blocking state. Implementing a non-blocking API or a timeout feature for the `recv()` function would allow the program to continue executing even if no data is received, thus preventing it from getting stuck and improving the robustness of the network communication process. This feature would be particularly beneficial in scenarios where network conditions are unreliable or when integrating with systems that require non-blocking operations.  
- [View Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/132)  


### OPC UA library for W5100S

- **Suggestion**: **Feature Request or Technical Suggestion:**

The user is requesting support or guidance for using the W5100S-EVB-PICO as an OPC UA client, specifically inquiring about the availability of libraries compatible with the W5100S-EVB-PICO or how to adapt the open62541 library for this purpose.

**Background Explanation:**

OPC UA (Open Platform Communications Unified Architecture) is a machine-to-machine communication protocol for industrial automation. The request implies a need for the W5100S-EVB-PICO to support OPC UA client functionality, which would involve either developing a compatible library or adapting an existing one like open62541. This capability would enable the W5100S-EVB-PICO to communicate with other devices and systems using the OPC UA protocol, which is widely used in industrial settings for secure and reliable data exchange.  
- [View Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/125)  


### Packet size in MQTT

- **Suggestion**: The core feature request or technical suggestion is:

"Support for handling packet sizes larger than the maximum socket buffer size (16KB) in the W5500 chip, potentially through fragmentation and reassembly or other means."

Background explanation:

The user is experiencing an issue where packets larger than the socket's dedicated buffer size (16KB) are not being received. This is a limitation of the W5500 chip, which has a total of 32KB of memory for all sockets. The user needs to handle data packets of about 40KB, which exceed the buffer capacity. A solution could involve implementing a mechanism to handle larger packets by fragmenting them into smaller chunks that fit within the buffer limits and then reassembling them, or by providing an alternative method to manage larger data transfers. This feature would enable the use of the W5500 chip in applications requiring the transmission of larger data packets, enhancing its functionality and applicability.  
- [View Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/114)  


### SPI._read_byte() is still used when SPI._read_burst() is defined

- **Suggestion**: The core feature request is to modify the `WIZCHIP_READ()` function logic to allow users to define only the burst variants of SPI operations without needing to implement the single-byte variants if they are not necessary. This would involve changing the function to check if the burst variant is defined and use it for single-byte operations if so.

Background Explanation:
The request suggests enhancing the flexibility of the SPI operation implementation in the WIZnet driver. Currently, even if a user defines the burst variant of SPI operations, they are still required to implement the single-byte variant (`_read_byte()`). This can be redundant if the burst operation can handle single-byte reads efficiently. By allowing the burst variant to be used for single-byte operations when defined, it simplifies the implementation for users who do not need separate single-byte operations, potentially reducing code duplication and improving maintainability. This change would be particularly beneficial for users working with platforms like STM32 HAL, where the burst operation might be more optimized or preferred.  
- [View Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/107)  


### socket.c infinite loop

- **Suggestion**: The core feature request or technical suggestion in the GitHub issue is:

**Feature Request: Implement a mechanism to prevent infinite loops in socket operations by introducing a timeout or retry limit.**

**Background Explanation:**
The issue highlights a problem with the current implementation of the `_socket()` and `_close()` functions, where an infinite loop is used to check the `Sn_CR` register. This can lead to the system getting stuck if the W5100 chip does not respond or is not connected to the MCU. The proposed solution involves adding a retry mechanism with a limit to prevent the infinite loop, which would return a timeout error if the limit is exceeded. This change is crucial for bare-metal programming environments where infinite loops can cause the system to hang, leading to communication failures and system instability. Implementing a timeout mechanism would enhance the robustness and reliability of the network operations in such environments.  
- [View Issue](https://github.com/Wiznet/ioLibrary_Driver/issues/94)  


