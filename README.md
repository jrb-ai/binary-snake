# binary-snake

Snake for macOS on Apple Silicon, written as raw machine code. No compiler, assembler or linker was used. The program is **1,498 bytes**, and each one is written out in `snake.bits` as 8 binary digits with a comment.

## Byte count

| Part | Bytes |
|---|---:|
| Mach-O header and 9 load commands | 568 |
| ARM64 code (219 instructions) | 876 |
| Alignment padding after the code | 4 |
| Data: tiles, score label, terminal escape codes, "GAME OVER" | 42 |
| Empty string table in `__LINKEDIT` | 8 |
| **Total written by hand** | **1,498** |

The file on disk is larger. The `@4000` line in `snake.bits` pads with zero bytes so that `__LINKEDIT` starts on the next 16 KiB page, which gives 16,392 bytes. Then `codesign` adds an ad-hoc signature of 344 bytes, so `snake` is 16,736 bytes. macOS on Apple Silicon does not run an unsigned executable.

## How it was made

Claude Opus 5.5, an AI model by Anthropic, wrote the bytes from a prompt by JRB AI. It wrote the whole executable as hex in one file write, with the matching assembly in comments for the reader. It did not call an assembler. It encoded each instruction and each Mach-O field itself.

After the first build, the disassembler `otool -tv` checked the bytes against the comments. One of the 219 instructions was wrong: `mov x10, #0x188` was encoded as `mov x10, #0x1880`. That instruction word was corrected by hand. A script then rewrote each hex byte as 8 binary digits, and the rebuilt executable was byte-identical.

`build.py` is a bit loader, not an assembler. It knows no instructions or labels. It turns each group of 8 binary digits into one byte, applies the `@` padding and signs the file.

## Run

Needs macOS on Apple Silicon.

```
python3 build.py
./snake
```

Steer with w a s d or the arrow keys. Press q to quit.

The build is deterministic: `build.py` gives the same 16,736 bytes each time.

## Licence

Apache-2.0. See `LICENSE`.
