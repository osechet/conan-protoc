
import os
from conans import ConanFile


class ProtobufTestConan(ConanFile):
    """ Conan test package for protoc """

    settings = "os", "compiler", "build_type", "arch"
    requires = "Protoc/3.3.1@osechet/testing"   # FIXME
    generators = "cmake"

    def imports(self):
        self.copy("protoc.exe",        "bin", "bin")  # Windows
        self.copy("protoc",            "bin", "bin")  # Linux / Macos

    def test(self):
        self.run("%s --version" % os.path.join(".", "bin", "protoc"))
