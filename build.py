
from conan.packager import ConanMultiPackager

def main():
    """
    Main function.
    """

    builder = ConanMultiPackager(username="osechet", channel="testing",
                                 visual_versions=["10", "12", "14"])
    builder.add_common_builds(shared_option_name="Protobuf:shared")
    filtered_builds = []
    for settings, options, env_vars, build_requires in builder.builds:
        if settings["arch"] != "x86_64":
            continue

        filtered_builds.append([settings, options, env_vars, build_requires])

        if settings["compiler"] == "gcc":
            cxx11_settings = dict(settings)
            cxx11_settings["compiler.libcxx"] = "libstdc++11"
            filtered_builds.append([cxx11_settings, options, env_vars, build_requires])

    builder.builds = filtered_builds
    builder.run()

if __name__ == "__main__":
    main()
