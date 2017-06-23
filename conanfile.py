
import os
from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment
from conans.tools import os_info, SystemPackageTool


class ProtocConan(ConanFile):
    """ Conan package for protoc """
    name = "Protoc"
    version = "3.3.1"
    description = "Conan package for Protoc"
    _sha256 = '30f23a45c6f4515598702a6d19c4295ba92c4a635d7ad8d331a4db9fccff392d'
    _shared_lib_version = 10

    _source_dir = "protobuf-%s" % version
    url = "https://github.com/osechet/conan-protobuf.git"
    license = "https://github.com/google/protobuf/blob/master/LICENSE"
    requires = "zlib/1.2.11@conan/stable"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def source(self):
        download_filename = "v%s.tar.gz" % self.version
        tools.download('https://github.com/google/protobuf/archive/%s' % download_filename, download_filename)
        tools.check_sha256(download_filename, self._sha256)
        tools.unzip(download_filename)
        os.unlink(download_filename)

    def system_requirements(self):
        if os_info.is_linux:
            installer = SystemPackageTool()
            for pkg in ["autoconf", "automake", "libtool", "curl", "make", "g++", "unzip"]:
                installer.install(pkg)

    def build(self):
        if self.settings.os == "Windows":
            args = ['-Dprotobuf_BUILD_TESTS=OFF', '-DBUILD_SHARED_LIBS=OFF']
            if self.settings.compiler == "Visual Studio":
                args += ['-Dprotobuf_MSVC_STATIC_RUNTIME=ON']
            cmake = CMake(self.settings)
            cmake_dir = os.path.sep.join([self._source_dir, "cmake"])
            cmake.definitions["CMAKE_INSTALL_PREFIX"] = "%s/release" % self.build_folder
            self.run('cmake . %s %s' % (cmake.command_line, ' '.join(args)), cwd=cmake_dir)
            self.run("cmake --build . --target install %s" % cmake.build_config, cwd=cmake_dir)
        else:
            env = AutoToolsBuildEnvironment(self)
            with tools.environment_append(env.vars):
                cpus = tools.cpu_count()

                self.run("./autogen.sh", cwd=self._source_dir)

                self.output.info("prefix is: %s/release" % self.build_folder)
                args = ['--disable-dependency-tracking', '--with-zlib',
                        '--prefix=%s/release' % self.build_folder]

                self.run("./configure %s" % (' '.join(args)), cwd=self._source_dir)
                self.run("make -j %s install" % cpus, cwd=self._source_dir)

    def package(self):
        if self.settings.os == "Windows":
            self.copy("*.exe", "bin", "%s/release/bin" % self.build_folder, keep_path=False)
        else:
            self.output.info("prefix is: %s/release/bin" % self.build_folder)
            self.copy("protoc", "bin", "%s/release/bin" % self.build_folder, keep_path=False)
