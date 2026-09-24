#!/usr/bin/env python3
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICON = os.path.join(ROOT, "src/main/resources/assets/quickcords/icon.png")
LICENSE = os.path.join(ROOT, "LICENSE")

SETTINGS = """pluginManagement {
	repositories {
		maven {
			name = 'Fabric'
			url = 'https://maven.fabricmc.net/'
		}
		mavenCentral()
		gradlePluginPortal()
	}
}

rootProject.name = 'quickcords'
"""

MOD_ID_CLASS = """package com.maxk.quickcords;

public final class QuickCords {
	public static final String MOD_ID = "quickcords";

	private QuickCords() {
	}
}
"""

ID_CLASS = """package com.maxk.quickcords;

import {id_import};

public final class QuickCords {{
	public static final String MOD_ID = "quickcords";

	private QuickCords() {{
	}}

	public static {id_type} id(String path) {{
		return {id_factory};
	}}
}}
"""

CLIENT_OLD = """package com.maxk.quickcords.client;

import com.mojang.blaze3d.platform.InputConstants;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.fabricmc.fabric.api.client.keybinding.v1.KeyBindingHelper;
import net.minecraft.client.KeyMapping;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import org.lwjgl.glfw.GLFW;

public class QuickCordsClient implements ClientModInitializer {
	private static KeyMapping copyCoordsKey;

	@Override
	public void onInitializeClient() {
		copyCoordsKey = KeyBindingHelper.registerKeyBinding(new KeyMapping(
			"key.quickcords.copy",
			InputConstants.Type.KEYSYM,
			GLFW.GLFW_KEY_C,
			"category.quickcords"
		));

		ClientTickEvents.END_CLIENT_TICK.register(client -> {
			while (copyCoordsKey.consumeClick()) {
				if (client.player == null) {
					continue;
				}

				BlockPos pos = client.player.blockPosition();
				String coords = pos.getX() + " " + pos.getY() + " " + pos.getZ();
				client.keyboardHandler.setClipboard(coords);
				client.player.displayClientMessage(Component.literal("Copied " + coords), true);
			}
		});
	}
}
"""

CLIENT_26 = """package com.maxk.quickcords.client;

import com.maxk.quickcords.QuickCords;
import com.mojang.blaze3d.platform.InputConstants;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.fabricmc.fabric.api.client.keymapping.v1.KeyMappingHelper;
import net.minecraft.client.KeyMapping;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import org.lwjgl.glfw.GLFW;

public class QuickCordsClient implements ClientModInitializer {
	private static final KeyMapping.Category CATEGORY = KeyMapping.Category.register(QuickCords.id("main"));
	private static KeyMapping copyCoordsKey;

	@Override
	public void onInitializeClient() {
		copyCoordsKey = KeyMappingHelper.registerKeyMapping(new KeyMapping(
			"key.quickcords.copy",
			InputConstants.Type.KEYSYM,
			GLFW.GLFW_KEY_C,
			CATEGORY
		));

		ClientTickEvents.END_CLIENT_TICK.register(client -> {
			while (copyCoordsKey.consumeClick()) {
				if (client.player == null) {
					continue;
				}

				BlockPos pos = client.player.blockPosition();
				String coords = pos.getX() + " " + pos.getY() + " " + pos.getZ();
				client.keyboardHandler.setClipboard(coords);
				client.player.sendOverlayMessage(Component.literal("Copied " + coords));
			}
		});
	}
}
"""

CLIENT_NEW = """package com.maxk.quickcords.client;

import com.maxk.quickcords.QuickCords;
import com.mojang.blaze3d.platform.InputConstants;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.fabricmc.fabric.api.client.keybinding.v1.KeyBindingHelper;
import net.minecraft.client.KeyMapping;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import org.lwjgl.glfw.GLFW;

public class QuickCordsClient implements ClientModInitializer {
	private static final KeyMapping.Category CATEGORY = KeyMapping.Category.register(QuickCords.id("main"));
	private static KeyMapping copyCoordsKey;

	@Override
	public void onInitializeClient() {
		copyCoordsKey = KeyBindingHelper.registerKeyBinding(new KeyMapping(
			"key.quickcords.copy",
			InputConstants.Type.KEYSYM,
			GLFW.GLFW_KEY_C,
			CATEGORY
		));

		ClientTickEvents.END_CLIENT_TICK.register(client -> {
			while (copyCoordsKey.consumeClick()) {
				if (client.player == null) {
					continue;
				}

				BlockPos pos = client.player.blockPosition();
				String coords = pos.getX() + " " + pos.getY() + " " + pos.getZ();
				client.keyboardHandler.setClipboard(coords);
				client.player.displayClientMessage(Component.literal("Copied " + coords), true);
			}
		});
	}
}
"""

LANG_OLD = """{
	"key.quickcords.copy": "Copy Coordinates",
	"category.quickcords": "Quick Cords"
}
"""

LANG_NEW = """{
	"key.quickcords.copy": "Copy Coordinates",
	"key.category.quickcords.main": "Quick Cords"
}
"""

FABRIC_MOD = """{{
	"schemaVersion": 1,
	"id": "quickcords",
	"version": "${{version}}",
	"name": "Quick Cords",
	"description": "Copy your coordinates with one key. Default is C; rebind it in Options → Controls → Quick Cords.",
	"authors": [
		"Meqxs"
	],
	"license": "MIT",
	"icon": "assets/quickcords/icon.png",
	"environment": "client",
	"entrypoints": {{
		"client": [
			"com.maxk.quickcords.client.QuickCordsClient"
		]
	}},
	"depends": {{
		"fabricloader": "{loader_dep}",
		"minecraft": "{mc_dep}",
		"java": "{java_dep}",
		"fabric-api": "*"
	}}
}}
"""

BUILD_REMAP = """plugins {{
	id 'net.fabricmc.fabric-loom-remap' version "${{loom_version}}"
	id 'maven-publish'
}}

base {{
	archivesName = 'quickcords-{mc}'
}}

loom {{
	splitEnvironmentSourceSets()

	mods {{
		"quickcords" {{
			sourceSet sourceSets.main
			sourceSet sourceSets.client
		}}
	}}
}}

dependencies {{
	minecraft "com.mojang:minecraft:${{project.minecraft_version}}"
	mappings loom.officialMojangMappings()
	modImplementation "net.fabricmc:fabric-loader:${{project.loader_version}}"
	modImplementation "net.fabricmc.fabric-api:fabric-api:${{project.fabric_api_version}}"
}}

processResources {{
	def version = project.version
	inputs.property "version", version

	filesMatching("fabric.mod.json") {{
		expand "version": version
	}}
}}

tasks.withType(JavaCompile).configureEach {{
	it.options.release = {java_release}
}}

java {{
	withSourcesJar()
	sourceCompatibility = JavaVersion.VERSION_{java_release}
	targetCompatibility = JavaVersion.VERSION_{java_release}
}}

jar {{
	def projectName = project.name
	inputs.property "projectName", projectName

	from("LICENSE") {{
		rename {{ "${{it}}_$projectName" }}
	}}
}}
"""

BUILD_26 = """plugins {{
	id 'net.fabricmc.fabric-loom' version "${{loom_version}}"
	id 'maven-publish'
}}

base {{
	archivesName = 'quickcords-{mc}'
}}

loom {{
	splitEnvironmentSourceSets()

	mods {{
		"quickcords" {{
			sourceSet sourceSets.main
			sourceSet sourceSets.client
		}}
	}}
}}

dependencies {{
	minecraft "com.mojang:minecraft:${{project.minecraft_version}}"
	implementation "net.fabricmc:fabric-loader:${{project.loader_version}}"
	implementation "net.fabricmc.fabric-api:fabric-api:${{project.fabric_api_version}}"
}}

processResources {{
	def version = project.version
	inputs.property "version", version

	filesMatching("fabric.mod.json") {{
		expand "version": version
	}}
}}

tasks.withType(JavaCompile).configureEach {{
	it.options.release = {java_release}
}}

java {{
	withSourcesJar()
	sourceCompatibility = JavaVersion.VERSION_{java_release}
	targetCompatibility = JavaVersion.VERSION_{java_release}
}}

jar {{
	def projectName = project.name
	inputs.property "projectName", projectName

	from("LICENSE") {{
		rename {{ "${{it}}_$projectName" }}
	}}
}}
"""

PROPS = """org.gradle.jvmargs=-Xmx1G
org.gradle.parallel=true
org.gradle.configuration-cache=false

minecraft_version={mc}
loader_version=0.19.5
loom_version=1.17-SNAPSHOT

version=1.0.0
group=com.maxk

fabric_api_version={fabric_api}
"""

VERSIONS = [
	{
		"mc": "1.20.4",
		"fabric_api": "0.97.3+1.20.4",
		"java_release": 17,
		"loader_dep": ">=0.15.0",
		"mc_dep": "~1.20.4",
		"java_dep": ">=17",
		"style": "old",
		"build": "remap",
	},
	{
		"mc": "1.21.8",
		"fabric_api": "0.136.1+1.21.8",
		"java_release": 21,
		"loader_dep": ">=0.16.0",
		"mc_dep": "~1.21.8",
		"java_dep": ">=21",
		"style": "old",
		"build": "remap",
	},
	{
		"mc": "1.21.11",
		"fabric_api": "0.141.6+1.21.11",
		"java_release": 21,
		"loader_dep": ">=0.19.2",
		"mc_dep": "~1.21.11",
		"java_dep": ">=21",
		"style": "new",
		"build": "remap",
		"id_import": "net.minecraft.resources.Identifier",
		"id_type": "Identifier",
		"id_factory": "Identifier.fromNamespaceAndPath(MOD_ID, path)",
	},
	{
		"mc": "26.1",
		"fabric_api": "0.145.1+26.1",
		"java_release": 25,
		"loader_dep": ">=0.19.2",
		"mc_dep": "~26.1",
		"java_dep": ">=25",
		"style": "new",
		"build": "26",
		"id_import": "net.minecraft.resources.Identifier",
		"id_type": "Identifier",
		"id_factory": "Identifier.fromNamespaceAndPath(MOD_ID, path)",
	},
]


def write(path, content):
	os.makedirs(os.path.dirname(path), exist_ok=True)
	with open(path, "w", newline="\n") as f:
		f.write(content)


def setup(v):
	base = os.path.join(ROOT, "versions", v["mc"])
	if os.path.exists(base):
		shutil.rmtree(base)

	write(os.path.join(base, "settings.gradle"), SETTINGS)
	write(os.path.join(base, "gradle.properties"), PROPS.format(**v))

	if v["build"] == "26":
		write(os.path.join(base, "build.gradle"), BUILD_26.format(**v))
	else:
		write(os.path.join(base, "build.gradle"), BUILD_REMAP.format(**v))

	write(
		os.path.join(base, "src/main/resources/fabric.mod.json"),
		FABRIC_MOD.format(**v),
	)
	write(
		os.path.join(base, "src/main/resources/assets/quickcords/lang/en_us.json"),
		LANG_NEW if v["style"] == "new" else LANG_OLD,
	)

	if v["style"] == "new":
		write(
			os.path.join(base, "src/main/java/com/maxk/quickcords/QuickCords.java"),
			ID_CLASS.format(**v),
		)
		write(
			os.path.join(base, "src/client/java/com/maxk/quickcords/client/QuickCordsClient.java"),
			CLIENT_26 if v["mc"] == "26.1" else CLIENT_NEW,
		)
	else:
		write(
			os.path.join(base, "src/main/java/com/maxk/quickcords/QuickCords.java"),
			MOD_ID_CLASS,
		)
		write(
			os.path.join(base, "src/client/java/com/maxk/quickcords/client/QuickCordsClient.java"),
			CLIENT_OLD,
		)

	shutil.copy2(LICENSE, os.path.join(base, "LICENSE"))
	dest_icon = os.path.join(base, "src/main/resources/assets/quickcords/icon.png")
	os.makedirs(os.path.dirname(dest_icon), exist_ok=True)
	shutil.copy2(ICON, dest_icon)
	print("created", base)


if __name__ == "__main__":
	for version in VERSIONS:
		setup(version)
