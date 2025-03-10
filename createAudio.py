"""
pip install -U kokoro-onnx soundfile

wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
python createAudio.py
"""
import soundfile as sf
from kokoro_onnx import Kokoro

kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")
samples, sample_rate = kokoro.create(
    """Unix (trademarked as UNIX) is a family of multitasking, multi-user computer operating systems that derive from the original AT&T Unix, whose development started in 1969[1] at the Bell Labs research center by Ken Thompson, Dennis Ritchie, and others.[4] Initially intended for use inside the Bell System, AT&T licensed Unix to outside parties in the late 1970s, leading to a variety of both academic and commercial Unix variants from vendors including University of California, Berkeley (BSD), Microsoft (Xenix), Sun Microsystems (SunOS/Solaris), HP/HPE (HP-UX), and IBM (AIX).

The early versions of Unix—which are retrospectively referred to as 'Research Unix'—ran on computers such as the PDP-11 and VAX; Unix was commonly used on minicomputers and mainframes from the 1970s onwards.[5] It distinguished itself from its predecessors as the first portable operating system: almost the entire operating system is written in the C programming language (in 1973), which allows Unix to operate on numerous platforms.[6] Unix systems are characterized by a modular design that is sometimes called the 'Unix philosophy'. According to this philosophy, the operating system should provide a set of simple tools, each of which performs a limited, well-defined function.[7] A unified and inode-based filesystem and an inter-process communication mechanism known as 'pipes' serve as the main means of communication,[4] and a shell scripting and command language (the Unix shell) is used to combine the tools to perform complex workflows.

Version 7 in 1979 was the final widely released Research Unix, after which AT&T sold UNIX System III, based on Version 7, commercially in 1982; to avoid confusion between the Unix variants, AT&T combined various versions developed by others and released it as UNIX System V in 1983. However as these were closed-source, the University of California, Berkeley continued developing BSD as an alternative. Other vendors that were beginning to create commercialized versions of Unix would base their version on either System V (like Silicon Graphics's IRIX) or BSD (like SunOS). Amid the 'Unix wars' of standardization, AT&T alongside Sun merged System V, BSD, SunOS and Xenix, soldifying their features into one package as UNIX System V Release 4 (SVR4) in 1989, and it was commercialized by Unix System Laboratories, an AT&T spinoff.[8][9] A rival Unix by other vendors was released as OSF/1, however most commercial Unix vendors eventually changed their distributions to be based on SVR4 with BSD features added on top.""", voice="af_sarah", speed=1.0, lang="en-us"
)
sf.write("audio.mp3", samples, sample_rate)
print("Created audio.wav")
