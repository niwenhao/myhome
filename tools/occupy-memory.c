/**
 * This is a sample program, It will keep allocating specified size of memory until exit.
 * This is useful to test the memory usage of the system.
 * The first parameter is the size of memory to allocate in MB.
 * The second parameter is the time to arrive the specified memory size in seconds. It should allocate (size/time) MB per second and allocate all memory in the specified time.
 */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    if (argc < 3) {
        printf("Usage: %s <size_in_MB> <time_to_allocate_in_sec>\n", argv[0]);
        return 1;
    }

    int size = atoi(argv[1]);
    int time_to_allocate = atoi(argv[2]);
    int time_to_keep_allocated = (argc >= 4) ? atoi(argv[3]) : -1;

    int total_size = size;
    int allocation_size = total_size / time_to_allocate;

    int allocated_size = 0;
    int seconds = 0;
    while (allocated_size < total_size) {
        printf("alloc -> ");
        char *buffer = malloc(allocation_size*1024*1024);
        if (buffer == NULL) {
            printf("Failed to allocate memory\n");
            break;
        }

        printf("clear -> ");
        for (int i = 0; i < allocation_size*1024*1024; i+=32) {
            buffer[i] = 0;
        }

        allocated_size += allocation_size;
        seconds++;
        printf("allocated %d MB, %d MB in %d seconds\n", allocated_size, allocation_size, seconds);
        sleep(1);
    }

    while (1) {
        sleep(1);
    }
    return 0;
}