#Website Connection Tester
#version: 0.0.1

import asyncio
import pathlib
import sys

from checker import server_response, server_response_async
from cli import display_check_result, cli_arg


def main():
    """Run RP Checker."""
    user_args = cli_arg()
    urls = _get_websites_urls(user_args)
    if not urls:
        print("Error: no URLs to check", file=sys.stderr)
        sys.exit(1)

    if user_args.asynchronous:
        asyncio.run(_asynchronous_check(urls))
    else:
        _synchronous_check(urls)


def _get_websites_urls(user_args):
    urls = user_args.urls
    if user_args.input_file:
        urls += _read_urls_from_file(user_args.input_file)
    return urls


def _read_urls_from_file(file):
    file_path = pathlib.Path(file)
    if file_path.is_file():
        with file_path.open() as urls_file:
            urls = [url.strip() for url in urls_file]
            if urls:
                return urls
            print(f"Error: empty input file, {file}", file=sys.stderr)
    else:
        print("Error: input file not found", file=sys.stderr)
    return []


async def _asynchronous_check(urls):
    async def _check(url):
        error = ""
        try:
            result = await server_response_async(url)
        except Exception as e:
            result = False
            error = str(e)
        display_check_result(result, url, error)

    await asyncio.gather(*(_check(url) for url in urls))


def _synchronous_check(urls):
    for url in urls:
        error = ""
        try:
            result = server_response(url)
        except Exception as e:
            result = False
            error = str(e)
        display_check_result(result, url, error)


if __name__ == "__main__":
    main()
