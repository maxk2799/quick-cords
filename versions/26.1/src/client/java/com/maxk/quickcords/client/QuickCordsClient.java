package com.maxk.quickcords.client;

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
