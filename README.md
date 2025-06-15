# Zource - Zig wrapper around the Source engine

HEAVILY WIP at the moment.

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/thetredev/zource)

## The Plan

Reimplement Source.Python (https://github.com/Source-Python-Dev-Team/Source.Python) using Zig (https://ziglang.org/) and Ziggy Pydust (https://pydust.fulcrum.so/latest/) as the bridge layer for Python (https://python.org/) instead of C++ (https://cppreference.com/) and Boost.Python (https://www.boost.org/doc/libs/latest/libs/python/doc/html/index.html).

## How?

- Understand how Source.Python works internally
- Implement stuff one by one in Zig (not the whole thing)

## When to expect releases?

Not very soon...

## Implementation Overview

The codebase will be split up across multile programming languages, each responsible for its own layer. It will look something along the lines of:

| Programming Language / Layer | Purpose / Responsibility |
| --- | --- |
| C++ | Plugin shim layer to forward Source SDK objects and function calls to the C ABI and back via `extern "C"`. This effecively abstracts away the object oriented design used heavily in the Source SDK, streamlining it down into simple building blocks like structs and functions. |
| C ABI | Compiled plugin shim layer which contains unmangled symbol names for Zig to interact with. |
| Zig | Build system and core Zource implementation layer. Exposes the Source SDK to Python over the C ABI.\* |
| Python | Primary user facing API to write plugins in.\* |

\* In the future, depending on how everything will actually work together in the end, the Zig implementation can be used to expose the Source SDK over some kind of socket as the *Zource SDK*, which would allow us to implement client SDKs for that in a variety of languages and removes the need to create Python modules directly in a lower level (C++/Zig) entirely. I will not go that route until Zource v1 is stabilized, though. The first step is to basically modernize Source.Python primarily for Counter-Strike: Source, because I'm most familiar with that specific game. Afterwards we'll see how to move forward.
