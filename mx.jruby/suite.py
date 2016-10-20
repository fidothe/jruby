# Copyright (c) 2016 Oracle and/or its affiliates. All rights reserved. This
# code is released under a tri EPL/GPL/LGPL license. You can use it,
# redistribute it and/or modify it under the terms of the:
#
# Eclipse Public License version 1.0
# GNU General Public License version 2
# GNU Lesser General Public License version 2.1

def mavenLib(mavenDep, sha1, sourceSha1, license):
    groupId, artifactId, version = mavenDep.split(':')
    args = (groupId.replace('.', '/'), artifactId, version, artifactId, version)
    base = "https://search.maven.org/remotecontent?filepath=%s/%s/%s/%s-%s" % args
    url = base + ".jar"
    sourceUrl = base + '-sources.jar'
    return {
        "urls": [ url ],
        "sha1": sha1,
        "sourceUrls": [ sourceUrl ],
        "sourceSha1": sourceSha1,
        "maven": {
            "groupId": groupId,
            "artifactId": artifactId,
            "version": version,
        },
        "license": license
    }

suite = {
    "mxversion": "5.51.0",
    "name": "jrubytruffle",

    "imports": {
        "suites": [
            {
                "name": "truffle",
                # Must be the same as in truffle/pom.rb (except for the -SNAPSHOT part only in pom.rb, and there we can use a release name)
                "version": "af21c6632dbc4e8c48cd25d0b7d623d379c888e6",
                "urls": [
                    {"url": "https://github.com/graalvm/truffle.git", "kind": "git"},
                    {"url": "https://curio.ssw.jku.at/nexus/content/repositories/snapshots", "kind": "binary"},
                ]
            },
        ],
    },

    "licenses": {
        "EPL-1.0": {
            "name": "Eclipse Public License 1.0",
            "url": "https://opensource.org/licenses/EPL-1.0",
        },
        "BSD-simplified" : {
          "name" : "Simplified BSD License (2-clause BSD license)",
          "url" : "http://opensource.org/licenses/BSD-2-Clause"
        },
        "MIT" : {
          "name" : "MIT License",
          "url" : "http://opensource.org/licenses/MIT"
        },
        "Apache-2.0" : {
          "name" : "Apache License 2.0",
          "url" : "https://opensource.org/licenses/Apache-2.0"
        },
        "GPLv2" : {
          "name" : "GNU General Public License, version 2",
          "url" : "http://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html"
        },
        "zlib" : {
          "name" : "The zlib License",
          "url" : "https://opensource.org/licenses/zlib"
        },
    },

    "libraries": {

        # ------------- Libraries -------------

        "ANTLR4_RUNTIME": mavenLib(
            "org.antlr:antlr4-runtime:4.5.1-1",
            "66144204f9d6d7d3f3f775622c2dd7e9bd511d97",
            "e0057705e96c77719e7d49cb64dc014d023e7a9b",
            "BSD-new"),

        "SNAKEYAML": mavenLib(
            "org.yaml:snakeyaml:1.14",
            "c2df91929ed06a25001939929bff5120e0ea3fd4",
            "4c6bcedc3efa772a5ae1c2fd01efee8e4d15edac",
            "Apache-2.0"),
    },

    "projects": {

        # ------------- Projects -------------

        "jruby-core": {
            "class": "JRubyCoreMavenProject",
            "sourceDirs": [ "core/src/main/java" ],
            "watch": [ "core/src" ],
            "jar": "lib/jruby.jar",
            "license": [ "EPL-1.0", "BSD-new", "BSD-simplified", "MIT", "Apache-2.0" ],
        },

        "jruby-truffle": {
            "dir": "truffle/src/main",
            "sourceDirs": [ "java" ],
            "dependencies": [
                "jruby-core",
                "truffle:TRUFFLE_API",
                "truffle:TRUFFLE_DEBUG",
                "ANTLR4_RUNTIME",
                "SNAKEYAML",
            ],
            "annotationProcessors": ["truffle:TRUFFLE_DSL_PROCESSOR"],
            "javaCompliance": "1.8",
            "workingSets": "JRubyTruffle",
            "checkPackagePrefix": "false",
            "license": [ "EPL-1.0", "BSD-new", "BSD-simplified", "MIT", "Apache-2.0" ],
        },

        "jruby-truffle-ruby": {
            "class": "ArchiveProject",
            "outputDir": "truffle/src/main/ruby",
            "prefix": "jruby-truffle",
            "license": [ "EPL-1.0", "BSD-new" ],
        },

        "jruby-truffle-test": {
            "dir": "truffle/src/test",
            "sourceDirs": ["java"],
            "dependencies": [
                "jruby-truffle",
                "truffle:TRUFFLE_TCK",
                "mx:JUNIT",
            ],
            "javaCompliance": "1.8",
            "checkPackagePrefix": "false",
            "license": "EPL-1.0",
        },

        "jruby-truffle-ruby-test": {
            "class": "ArchiveProject",
            "outputDir": "truffle/src/test/ruby",
            "prefix": "src/test/ruby",
            "license": "EPL-1.0",
        },

        # Depends on jruby-core extracting jni libs in lib/jni
        "jruby-lib-jni": {
            "class": "ArchiveProject",
            "outputDir": "lib/jni",
            "prefix": "lib/jni",
            "dependencies": [ "jruby-core" ],
            "license": [ "Apache-2.0", "MIT" ],
        },

        # Depends on jruby-core installing gems in lib/ruby
        "jruby-lib-ruby": {
            "class": "ArchiveProject",
            "outputDir": "lib/ruby",
            "prefix": "lib/ruby",
            "dependencies": [ "jruby-core" ],
            "license": [ "EPL-1.0", "MIT", "BSD-simplified", "GPLv2", "LGPLv21", "zlib" ],
        },

        "jruby-licenses": {
            "class": "LicensesProject",
            "outputDir": "",
            "prefix": "",
        },
    },

    "distributions": {

        # ------------- Distributions -------------

        "RUBY": {
            "mainClass": "org.jruby.Main",
            "dependencies": [
                "jruby-core",
                "jruby-truffle",
                "jruby-truffle-ruby",
            ],
            "exclude": [
                "truffle:JLINE",
            ],
            "distDependencies": [
                "truffle:TRUFFLE_API",
                "truffle:TRUFFLE_DEBUG",
            ],
            "description": "JRuby+Truffle",
            "license": [ "EPL-1.0", "BSD-new", "BSD-simplified", "MIT", "Apache-2.0" ],
        },

        # Set of extra files to extract to run Ruby
        "RUBY-ZIP": {
            "native": True, # Not Java
            "relpath": True,
            "dependencies": [
                "jruby-lib-jni",
                "jruby-lib-ruby",
                "jruby-licenses",
            ],
            "overlaps": [
                "RUBY",
            ],
            "description": "JRuby+Truffle Native Libs",
            "license": [ "EPL-1.0", "MIT", "BSD-simplified", "GPLv2", "LGPLv21", "zlib" ],
        },

        "RUBY-TEST": {
            "dependencies": [
                "jruby-truffle-test",
                "jruby-truffle-ruby-test",
            ],
            "exclude" : [
                "mx:HAMCREST",
                "mx:JUNIT"
            ],
            "distDependencies": [
                "RUBY",
                "truffle:TRUFFLE_TCK"
            ],
            "license": "EPL-1.0",
        },
    },
}
