package com.maxk.quickcords;

import net.minecraft.resources.Identifier;

public final class QuickCords {
	public static final String MOD_ID = "quickcords";

	private QuickCords() {
	}

	public static Identifier id(String path) {
		return Identifier.fromNamespaceAndPath(MOD_ID, path);
	}
}
