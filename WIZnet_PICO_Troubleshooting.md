### 🔧 UDP Server Example, debug print missing

1. 문제 현상:
시리얼 터미널에서 네트워크 구성 정보만 출력되고 디버그 출력이 나오지 않음

2. 원인:
UART/USB 디버그 printf 문이 활성화되지 않음

3. 해결 방법:
UART/USB 디버그 printf 문을 활성화하는 방법을 찾아서 적용해야 함.

[GitHub 이슈 보기](https://github.com/WIZnet-ioNIC/WIZnet-PICO-C/issues/10)


### 🔧 Failed compilation on Linux Evironment

1. 문제 현상:
make를 실행한 후 다음과 같은 문제가 발생합니다.
/usr/lib/gcc/arm-none-eabi/10.3.1/../../../arm-none-eabi/bin/ld: CMakeFiles/w5x00_tftp_client.dir/__/__/libraries/ioLibrary_Driver/Internet/TFTP/tftp.c.obj: in function `recv_tftp_data':
/home/pico/turoswiz/WIZnet-PICO-C/libraries/ioLibrary_Driver/Internet/TFTP/tftp.c:440: undefined reference to `save_data'
/usr/lib/gcc/arm-none-eabi/10.3.1/../../../arm-none-eabi/bin/ld: /home/pico/turoswiz/WIZnet-PICO-C/libraries/ioLibrary_Driver/Internet/TFTP/tftp.c:423: undefined reference to `save_data'
collect2: error: ld returned 1 exit status
make[2]: *** [examples/tftp/CMakeFiles/w5x00_tftp_client.dir/build.make:1520: examples/tftp/w5x00_tftp_client.elf] Error 1
make[1]: *** [CMakeFiles/Makefile2:2745: examples/tftp/CMakeFiles/w5x00_tftp_client.dir/all] Error 2
make: *** [Makefile:136: all] Error 2

2. 원인:
save_data 함수에 대한 참조가 정의되지 않았습니다.

3. 해결 방법:
save_data 함수를 정의하거나, 해당 함수에 대한 참조를 올바르게 설정하여 문제를 해결할 수 있습니다.

[GitHub 이슈 보기](https://github.com/WIZnet-ioNIC/WIZnet-PICO-C/issues/9)


### 🔧 How to add correctly the mbedtls project as submodule

1. 문제 현상: mbedtls를 서브모듈로 추가한 후 CMake이 구성할 때 일부 파일이 누락되어 오류가 발생함.
2. 원인: mbedtls 폴더가 libraries 폴더 안에 없어서 발생한 문제.
3. 해결 방법: mbedtls 폴더를 libraries 폴더 안에 추가한 후 CMake을 다시 구성하거나 mbedtls 폴더 내에서 몇 번 업데이트를 시도해도 문제가 해결되지 않음. 올바르게 추가하는 방법을 알고 있는지 확인 요청.

[GitHub 이슈 보기](https://github.com/WIZnet-ioNIC/WIZnet-PICO-C/issues/8)


### 🔧 Issue: W55RP20-EVB-PICO Firmware Not Booting After Building

1. 문제 현상:
- W55RP20-EVB-PICO 보드의 펌웨어 빌드 및 플래싱 후 부팅 실패

2. 원인:
- Pico-SDK 1.5.0 버전을 사용하는데 필요한 파일이 부족하여 클럭 초기화 문제 발생

3. 해결 방법:
- 해당 레포지토리를 Pico-SDK 2.0.0으로 업데이트하거나, Pico-SDK 1.5.0과 호환되는 새로운 패치 제공하여 클럭 초기화 문제 해결 가능.

[GitHub 이슈 보기](https://github.com/WIZnet-ioNIC/WIZnet-PICO-C/issues/4)


