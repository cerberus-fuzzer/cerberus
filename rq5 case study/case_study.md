# Fuzzing on Real-World Code (RQ5)

## Runtime Error in a Stack Overflow Code Snippet

```python
from pytube import YouTube
link = input("Enter the link of YouTube video you want to download:  ")
yt = YouTube(link)
print("Title: ", yt.title)
print("Number of views: ", yt.views)
print("Length of video: ", yt.length)
print("Rating of video: ", yt.rating)
ys = yt.streams.get_highest_resolution()
print("Downloading...")
ys.download()
print("Download completed!!")
```

This case study demonstrates how "fuzzing" with **Cerberus** can uncover runtime errors in real-world code. The code snippet above is taken from a Stack Overflow post (#76654129). This Python script uses the `pytube` library to download a YouTube video by prompting the user for the URL. It retrieves the YouTube video and displays metadata.

### Identified Runtime Errors

This snippet contains two notable runtime errors:

1. **`ModuleNotFoundError`**: Triggered by the call to `YouTube(link)` at **line 3** when an invalid URL is provided as input. A fuzzer aims to generate a YouTube link input that causes this runtime error.

2. **`RegexMatchError`**: Caused by a bug in `pytube`'s internal function `get_throttling_function_name`. This exception occurs immediately after executing the import statement at **line 1** (`from pytube import YouTube`). As a result, any fuzzer relying on actual execution will fail to progress beyond this line and will not detect the `ModuleNotFoundError` exception.

### How Fuzzing with **Cerberus** Handles This Case

When this snippet was fuzzed with **Cerberus**, it generated the following YouTube URL inputs:

1. `https://www.youtube.com/watch?v=INVALIDLINK` – This input bypasses the import statement and detects the `ModuleNotFoundError` at line 3 (`YouTube(link)`).

2. `"Test1234"` – This input triggers the `RegexMatchError` and highlights the `import` statement as the root cause of the error.

### Conclusion

This case study illustrates that **Cerberus** can effectively handle incomplete or buggy code snippets. By leveraging pre-trained knowledge, **LLMs** can reason about API behaviors even in the presence of errors at the initial execution stage. Traditional fuzzers that rely solely on execution fail in such scenarios.
