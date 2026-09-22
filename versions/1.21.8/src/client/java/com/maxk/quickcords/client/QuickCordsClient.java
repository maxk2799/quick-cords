package com.maxk.quickcords.client;

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
