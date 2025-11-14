"""
XBot v2.1 - Complete Decompiled Source Code
Reconstructed from Python 3.13 bytecode
For defensive analysis and understanding attack techniques
"""

# =============================================================================
# IMPORTS
# =============================================================================

import math
import asyncio
from asyncio import AsyncRunner
import httpx
import re
from datetime import datetime, timedelta
import keyring
import uuid
import json
import flet as ft
from pathlib import Path

# =============================================================================
# CONFIGURATION
# =============================================================================

VERSION = "XBot V2.1"
SERVICE_CLIENT_ID = "XBot"
SERVICE_PASSWORD = "XBot.py"
PROFILES_FILE = ".xbot_profiles.json"
SETTINGS_FILE = ".settings.json"


# =============================================================================
# XBOTAPP
# =============================================================================

class XBotApp:
    """
    XBotApp class - reconstructed from bytecode
    """

    def __init__(self):
        # Local variables: SERVICE_CLIENT_ID, SERVICE_PASSWORD
        # Uses: saved_profiles, states, ui, accounts, all_settings, show_keys, AsyncRunner, runner, page, license_column
        pass

    def _add_license_to_data(self, license_key, browser_id, model, expiry_date, link_remote):
        # Local variables: lic_type, new_entry
        # Uses: accounts, append, page, run_task
        pass

    def _avg_hex(self, colors_hex):
        # Local variables: to_rgb, rs, gs, bs, c, r, g, b, n
        # Uses: IDLE, len, format
        pass

    def _avg_hex(h):
        # Uses: lstrip, int
        pass

    async def _check_license(self, key):
        # Local variables: client, r
        # Uses: httpx, AsyncClient, get, API_BASE, status_code, json, Exception
        pass

    def _configure_page_window(self, page):
        # Uses: title, window_width, window_height, window, width, height, resizable, maximizable, padding, margin
        # Important strings:
        # 'https://rsms.me/inter/font-files/Inter-Regular.otf?v=3.19'
        pass

    def _ensure_pid_state(self, pid):
        # Uses: states
        pass

    def _fancy_button(self, text, width, on_click, colors):
        # Local variables: label, button
        # Uses: ft, Text, FontWeight, BOLD, Container, alignment, center, LinearGradient, Scale, FAST
        pass

    def _fatal_status_ui(self, pid, message):
        """
        
        Update status text for a given profile id (pid) in red
        and pause the bot.
        
        """
        # Local variables: ui
        # Uses: ui, get, value, color, update, page
        pass

    async def _handle_apply_coupon(self, e, ui, page):
        # Local variables: coupon, discounted_amount, ctrl
        # Uses: coupon_input, current, value, strip, amount_label, update, LOADING_QR, qr_image, src, asyncio
        pass

    async def _handle_crypto_click(self, e, ui, page):
        # Local variables: btn, payment_currency, ctrl, address, amount
        # Uses: control, set_selected_crypto, data, coupon_input, current, value, update, amount_label, expires_label, address_label
        # Important strings:
        # 'https://quickchart.io/qr?text='
        pass

    async def _idle_breathing(self, pid, dot, speed, strength):
        # Local variables: base, min_opacity, max_opacity, opacity, delta
        # Uses: asyncio, sleep, states, get, opacity, update
        pass

    def _license_card(self, lic, index):
        # Local variables: key, typ, tag, expanded, status_bar, icon, expand_icon, p, profiles, expiry_raw, expiry_dt, remaining_days, warn_color, icon_type, expiry_row, tag_row, license_key_row
        # Uses: get, states, ui, ft, Container, IDLE, alignment, top_center, Margin, margin
        pass

    def _license_of_pid(self, pid):
        # Local variables: lic
        # Uses: accounts, any, get
        pass

    async def _link_license_remote(self, license_key):
        # Local variables: client, e
        # Uses: httpx, AsyncClient, post, API_BASE, CLIENT_ID, Exception, print
        # Important strings:
        # '/clients/licenses/link'
        pass

    async def _load_profiles_local(self):
        """
        Load subprofiles from JSON if present.
        """
        # Local variables: f, content, e
        # Uses: os, path, exists, PROFILE_FILE, aiofiles, open, read, json, loads, Exception
        pass

    def _load_settings_local(self):
        """
        Load all_settings and saved_profiles from JSON (sync).
        """
        # Local variables: f, content, data, e
        # Uses: os, path, exists, SETTINGS_FILE, print, open, read, json, loads, all_settings
        pass

    def _open_edit_purchase_dialog(self, kind, pid):
        """
        
        kind: 'id' | 'model'
        Shows a dialog where user edits Browser ID or Model Name,
        applies it locally, then proceeds to payment.
        
        """
        # Local variables: hint, icon, on_close, on_proceed, proceed_button
        # Uses: ft, Icons, PERSON_OUTLINE, DEVICE_HUB, TextField, Padding, TextStyle, TEXT, Text, SUBTLE
        pass

    def _open_edit_purchase_dialog():
        # Local variables: val, lic, p, new_id, i
        # Uses: value, strip, accounts, get, int, enumerate, states, pop, ui
        pass

    def _open_edit_purchase_dialog(e):
        # Uses: page, dialog, open, update
        pass

    def _open_edit_purchase_dialog(e):
        # Local variables: price, detail
        # Uses: opacity, page, update, dialog, open, PRICES, get, value, strip
        pass

    def _open_edit_purchase_dialog():
        # Local variables: val
        # Uses: value, strip, startswith, isdigit, len
        pass

    def _profile_row(self, key, data, typ, model):
        # Local variables: dot, runtime_text, runtime, h, m, s, status_label, status_color, status, settings, drop_limit, drop_text, bar, on_run_click, run_text_val, run_colors, run_text, run_btn, edit_text, edit_btn, report_text, report_btn, remove_btn, confirm_remove, remove_text, right_controls
        # Uses: states, ft, Container, border_radius, only, Text, SUBTLE, bgcolor, BoxShadow, Offset
        pass

    def _profile_row(e):
        # Local variables: confirm_dialog
        # Uses: ft, AlertDialog, Text, FontWeight, W_600, TEXT, SUBTLE, TextButton, ButtonStyle, Colors
        pass

    def _profile_row():
        # Local variables: lic, p
        # Uses: accounts, any, get, page, dialog, open, run_task
        pass

    def _profile_row(e):
        # Local variables: pause_only, pause_all, should_show_pause_all, pause_dialog, a
        # Uses: get, lower, sum, accounts, ft, AlertDialog, Row, CrossAxisAlignment, CENTER, Icon
        pass

    def _profile_row(ev):
        # Local variables: lic, p, targets
        # Uses: page, dialog, open, update, accounts, get
        pass

    def _profile_row(ev):
        # Uses: page, dialog, open, update
        pass

    def _profile_row(pid):
        # Local variables: st, state, bot, e, dot, lic
        # Uses: states, get, print, stop, page, run_task, cleanup, Exception, cancel, ui
        pass

    def _profile_row(pids):
        # Local variables: p
        pass

    def _prompt_tag_input(self, key):
        # Local variables: save_tag
        # Uses: ft, TextField, AlertDialog, Text, Container, Colors, BLACK12, BoxShadow, with_opacity, BLACK87
        pass

    def _prompt_tag_input(e):
        # Uses: value, page, dialog, open, update
        pass

    def _render_bootstrap(self):
        """
        
        Rebuilds the original `bootstrap(page)` screen as class methods.
        Visuals/behavior unchanged.
        
        """
        # Local variables: TEXT_C, SUBTLE_C, ACCENT, saved_client_id, saved_password, toggle_new_visibility, toggle_existing_visibility, submit_new, submit_existing, layout, particles, animate_particles
        # Uses: page, keyring, get_password, CLIENT_ID, CLIENT_PASSWORD, run_task, ft, AlertDialog, Text, FontWeight
        pass

    def _render_bootstrap():
        # Uses: open, update
        pass

    def _render_bootstrap(msg):
        # Uses: content, value, dialog, open, update
        pass

    async def _render_bootstrap(e):
        # Local variables: cid, pw, client, res
        # Uses: value, strip, re, match, len, httpx, AsyncClient, post, API_BASE, print
        # Important strings:
        # '/clients/restore'
        pass

    async def _render_bootstrap(e):
        # Local variables: pw, cpw, cid, client, res
        # Uses: value, strip, len, str, uuid, uuid4, httpx, AsyncClient, post, API_BASE
        # Important strings:
        # '/clients/create'
        pass

    def _render_bootstrap(to):
        # Uses: visible, ft, ButtonStyle, style, update
        pass

    def _render_bootstrap(e):
        # Local variables: icon
        # Uses: ft, Icons, VISIBILITY_OFF, VISIBILITY, password, name, update
        pass

    def _render_bootstrap(e):
        # Local variables: icon
        # Uses: ft, Icons, VISIBILITY_OFF, VISIBILITY, password, name, update
        pass

    def _render_licenses(self):
        # Local variables: i, lic, card, key, active, paused, scheduled, p, pid, s
        # Uses: license_column, controls, clear, accounts, append, ft, Container, alignment, center, Column
        pass

    def _render_main_dashboard(self, restore):
        """
        
        Rebuilds the original `main(page, restore=False)` screen, wired to class state.
        
        """
        # Local variables: particles, animate_particles, layout
        # Uses: page, ft, Column, license_column, generate_shimmering_dust, Container, Row, MainAxisAlignment, SPACE_BETWEEN, Text
        pass

    async def _restore_licenses(self):
        # Local variables: client, res, data, licenses, local_profiles, lic, p, pid, key, license_data, entry, e
        # Uses: httpx, AsyncClient, post, API_BASE, CLIENT_ID, CLIENT_PASSWORD, status_code, print, json, Exception
        # Important strings:
        # '/clients/restore'
        pass

    def _run_automation(self, pid, state):
        # Local variables: l, settings, runner, future
        # Uses: accounts, any, get, all_settings, str, DEFAULT_SETTINGS, copy, DolphinBot, states, update_settings
        pass

    async def _run_automation():
        # Uses: run, get
        pass

    async def _running_glow(self, pid, dot, speed, strength):
        # Local variables: base, min_opacity, max_opacity, opacity, delta
        # Uses: ft, BoxShadow, Offset, shadow, bgcolor, states, get, opacity, update, asyncio
        pass

    async def _runtime_counter(self, pid, text_element):
        # Local variables: seconds, h, m, s
        # Uses: states, get, value, update, asyncio, sleep
        pass

    async def _save_profiles_local(self):
        """
        Persist subprofiles for Infinite licenses to JSON.
        """
        # Local variables: data, lic, p, f, e
        # Uses: accounts, get, aiofiles, open, PROFILE_FILE, write, json, dumps, Exception, print
        pass

    def _save_settings_local(self):
        """
        Persist all_settings and saved_profiles to JSON (sync).
        """
        # Local variables: data, f, e
        # Uses: all_settings, saved_profiles, open, SETTINGS_FILE, write, json, dumps, print, list, keys
        pass

    async def _scheduled_countdown(self, pid):
        # Local variables: ui_entry, dot, lic, remaining, mins, secs
        # Uses: states, get, ui, value, IDLE, color, update, ft, LinearGradient, SUCCESS
        pass

    def _set_paused(self, pid):
        # Local variables: dot, state, bot, e, lic
        # Uses: ui, states, get, print, stop, page, run_task, cleanup, Exception, cancel
        pass

    def _set_scheduled(self, pid, delay_minutes, skip_countdown):
        # Local variables: scheduled_breathing, lic
        # Uses: ui, states, datetime, now, timedelta, get, cancel, shadow, gradient, SCHEDULE
        pass

    async def _set_scheduled():
        # Local variables: base, min_opacity, max_opacity, opacity, delta
        # Uses: asyncio, sleep, states, get, opacity, update
        pass

    def _show_add_license_dialog(self):
        # Local variables: on_close, on_change, on_add
        # Uses: ft, TextField, TextStyle, TEXT, Text, FAST, Container, Padding, Row, MainAxisAlignment
        pass

    def _show_add_license_dialog(info):
        # Local variables: expiry, now
        # Uses: datetime, strptime, now, Exception
        pass

    def _show_add_license_dialog(e):
        # Local variables: info, browser_id, model, expiry
        # Uses: value, strip, any, accounts, opacity, page, update, dialog, open, get
        pass

    def _show_add_license_dialog(e):
        # Local variables: validate
        # Uses: value, strip, visible, any, accounts, opacity, page, update, re, match
        pass

    async def _show_add_license_dialog():
        # Local variables: info
        # Uses: value, visible, page, update
        pass

    def _show_add_license_dialog(e):
        # Uses: page, dialog, open, update
        pass

    def _show_add_profile_dialog(self, license_key):
        # Local variables: on_close, on_add, add_btn
        # Uses: ft, TextField, TextStyle, TEXT, Text, FAST, Container, ElevatedButton, Colors, CYAN_100
        pass

    def _show_add_profile_dialog(e):
        # Local variables: val, lic
        # Uses: value, strip, isdigit, len, opacity, page, update, int, any, accounts
        pass

    def _show_add_profile_dialog(e):
        # Uses: page, dialog, open, update
        pass

    def _show_health_status_popup(self, license_key):
        # Local variables: lic, expiry_raw, expiry_dt, remaining_days, expiry_text, expiry_icon_color, error_text, error_icon_color, ban_text, ban_icon_color, health_row
        # Uses: next, accounts, get, datetime, strptime, now, days, REPORT_COLOR, SUCCESS, ft
        pass

    def _show_health_status_popup(icon_color, title, value):
        # Uses: ft, Row, MainAxisAlignment, START, CrossAxisAlignment, CENTER, Icon, Icons, HEALTH_AND_SAFETY, Column
        pass

    def _show_license_type_popup(self, license_key):
        # Local variables: lic, descriptions, explanation, is_upgradeable, upgrade_price_key, on_upgrade_click, action_control
        # Uses: next, accounts, get, PRICES, ft, Container, Row, MainAxisAlignment, CENTER, Icon
        pass

    def _show_license_type_popup(e):
        # Uses: page, dialog, open, update
        pass

    def _show_purchase_license_dialog(self):
        # Local variables: proceed_to_payment, close_dialog, selector_button, addon1_sub, addon2_title, addon2_sub, confirm_button, close_icon
        # Uses: PRICES, ft, Text, TEXT, Row, FontWeight, BOLD, SUBTLE, Container, Column
        pass

    def _show_purchase_license_dialog(e):
        # Uses: page, dialog, open, update
        pass

    def _show_purchase_license_dialog(e):
        # Uses: page, dialog, open, update
        pass

    def _show_purchase_license_dialog():
        # Local variables: base_key, base_price, infinite_price, lifetime_price, total
        # Uses: PRICES, get, value, page, update
        pass

    def _show_purchase_license_dialog(label, is_selected, data_value):
        # Uses: ft, Container, Text, TEXT, alignment, center, LinearGradient, FAST, Scale
        pass

    def _show_purchase_license_dialog(addon, card):
        # Uses: bgcolor, ft, LinearGradient, alignment, top_center, bottom_center, gradient, page, update
        pass

    def _show_purchase_license_dialog(e, new_type):
        # Local variables: btn, selected
        # Uses: bgcolor, gradient, data, ft, LinearGradient, value, controls, page, update
        pass

    def _show_purchase_page(self, product, cost, details):
        """
        
        purchase_ui = self.PurchaseUI(
            on_crypto_click=lambda e: self.page.run_task(self._handle_crypto_click, e, purchase_ui, self.page),
            on_apply_coupon=lambda e: self.page.run_task(self._handle_apply_coupon, e, purchase_ui, self.page),
        )
        
        self.page.dialog = ft.AlertDialog(
            title=ft.Column(spacing=4, controls=[
                ft.Text(product + f" - Cost: {cost}$", size=16, weight=ft.FontWeight.BOLD),
                ft.Text(details or "", size=12, color=ft.Colors.GREY_400)
            ]),
            modal=False,
            content=ft.Container(content=purchase_ui.view(), height=290, width=685),
            actions=[ft.TextButton("Close", on_click=lambda e: (setattr(self.page.dialog, "open", False), self.page.update()))],
            actions_alignment=ft.MainAxisAlignment.END,
            content_padding=20,
        )
        self.page.dialog.open = True
        self.page.open(self.page.dialog)
        self.page.update()
        
        """
        # Uses: ft, AlertDialog, alignment, center, Container, Column, MainAxisAlignment, CENTER, CrossAxisAlignment, Icon
        pass

    def _show_renew_license_dialog(self, license_key):
        # Local variables: lic, renew_price_key, upgrade_price_key, expiry_raw, expiry_dt, remaining_days, expiry_label, icon_color, action_button, go_to_payment_lifetime, go_to_payment_renew, renew_btn, lifetime_btn, lifetime_message
        # Uses: next, accounts, get, PRICES, datetime, strptime, now, days, REPORT_COLOR, SUCCESS
        pass

    def _show_renew_license_dialog(icon, text, color, handler):
        # Uses: ft, Container, Row, MainAxisAlignment, CENTER, Icon, Text, FontWeight, BOLD, Padding
        pass

    def _show_renew_license_dialog(e):
        # Uses: page, dialog, open, update
        pass

    def _show_renew_license_dialog(e):
        # Uses: page, dialog, open, update
        pass

    def _show_run_confirmation_dialog(self, e, pid, typ, key):
        # Local variables: border_color, text_hint, run_all_colors, make_field, schedule_switch, alternate_switch, on_schedule_toggle, on_alternate_toggle, run_single, run_all, run_text, run_all_button, run_all_text, close_dialog, close_btn, options_column, c, actions_row, header_row, dialog_content
        # Uses: ft, Checkbox, Container, border_radius, only, border, all, padding, Column, Row
        pass

    def _show_run_confirmation_dialog(ev):
        # Uses: page, dialog, open, update
        pass

    def _show_run_confirmation_dialog(width, hint):
        # Uses: ft, TextField, TextAlign, CENTER, Padding
        pass

    def _show_run_confirmation_dialog(ev):
        # Uses: control, value, disabled, color, update
        pass

    def _show_run_confirmation_dialog(ev):
        # Uses: control, value, disabled, color, update
        pass

    def _show_run_confirmation_dialog(ev):
        # Local variables: lic, p, i, batch_delay, alternate_loop, delayed_all
        # Uses: page, dialog, open, update, accounts, get, int, value, strip, enumerate
        pass

    async def _show_run_confirmation_dialog():
        # Local variables: idx, batch, p
        # Uses: asyncio, sleep, range, len, states, get
        pass

    async def _show_run_confirmation_dialog():
        # Local variables: p
        # Uses: asyncio, sleep, states, get
        pass

    def _show_run_confirmation_dialog(ev):
        # Local variables: delayed
        # Uses: page, dialog, open, update, int, value, strip, ui, ft, LinearGradient
        pass

    async def _show_run_confirmation_dialog():
        # Uses: asyncio, sleep, states, get
        pass

    def _show_run_confirmation_dialog():
        # Uses: ft, LinearGradient, gradient, disabled, update
        pass

    def _show_run_confirmation_dialog():
        # Uses: ft, LinearGradient, gradient, bgcolor, update
        pass

    def _show_settings_dialog(self, pid, mode):
        # Local variables: dialog_mode, close_settings, toggle_randomize, toggle_no_gif, labeled_slider, labeled_dropdown, no_gif_check, drop_message_input, save_profile, group_box, basic_group, gif_group, message_group, leniency_bundle, advanced_group, header_title, mode_tabs, content_body, profile_group, save_settings_btn, save_icon_btn
        # Uses: str, all_settings, DEFAULT_SETTINGS, copy, ft, Column, TextField, TextStyle, TEXT, Checkbox
        pass

    def _show_settings_dialog(e):
        # Uses: page, dialog, open, update
        pass

    def _show_settings_dialog(name):
        # Uses: saved_profiles
        pass

    def _show_settings_dialog(title, content):
        # Uses: ft, Container, LinearGradient, Column, Text, FontWeight, BOLD, TEXT
        pass

    def _show_settings_dialog(label, options, default, key):
        # Local variables: v
        # Uses: ft, Column, Text, TEXT, Dropdown, dropdown, Option, str, TextStyle
        pass

    def _show_settings_dialog(label, min_val, max_val, default, key, suffix):
        # Uses: ft, Column, Text, TEXT, Slider
        pass

    def _show_settings_dialog(name):
        # Local variables: new_settings
        # Uses: saved_profiles, update
        pass

    def _show_settings_dialog():
        # Local variables: name
        # Uses: controls, clear, saved_profiles, append, ft, Row, MainAxisAlignment, SPACE_BETWEEN, Text, TEXT
        pass

    def _show_settings_dialog(e):
        # Local variables: _, profile, name
        # Uses: saved_profiles, items, all_settings, get, str, value, strip, copy
        pass

    def _show_settings_dialog(e):
        # Local variables: _, profile, base, i, name
        # Uses: saved_profiles, items, all_settings, get, str, copy
        pass

    def _show_settings_dialog(text, duration):
        # Local variables: fade
        # Uses: ft, Container, alignment, center, Text, Animation, controls, clear, append, page
        pass

    async def _show_settings_dialog():
        # Uses: asyncio, sleep, opacity, page, update
        pass

    def _show_settings_dialog(new_mode):
        # Uses: page, dialog, open
        pass

    def _show_settings_dialog(e):
        # Uses: control, value, disabled, page, update
        pass

    def _show_settings_dialog(e):
        # Uses: control, value, disabled, page, update
        pass

    def _toggle_license_key_visibility(self):
        # Uses: show_keys
        pass

    def _toggle_profiles(self, e, key):
        # Local variables: state
        # Uses: states, ui, visible, height, opacity, ft, Rotate, math, pi, rotate
        pass

    def _toggle_run(self, e, pid, mode, error_case):
        # Local variables: state, run, ui_entry, dot, lic
        # Uses: states, get, cancel, Exception, bool, ui, value, ft, LinearGradient, gradient
        pass

    def _update_bot_settings(self, pid):
        """
        Push latest settings into the running bot if it exists.
        """
        # Local variables: state, bot, settings
        # Uses: states, get, all_settings, str, DEFAULT_SETTINGS, copy, update_settings
        pass

    def _update_gif_progress(self, pid, count):
        # Local variables: ui, drop_limit
        # Uses: ui, get, all_settings, str, min, value, update, page
        pass

    def _update_license_status(self, license_key, override):
        # Local variables: hex_to_rgb, rgb_to_hex, license_data, p, profile_ids, error_color, avg_color, total, active, paused, scheduled, idle, color_map, color_sources, r_sum, g_sum, b_sum, count, has_error, pid, st, bar
        # Uses: next, accounts, get, len, SUCCESS, PAUSE_COLOR, IDLE, SCHEDULE, max, sum
        pass

    def _update_license_status(hex_color):
        # Uses: lstrip, tuple
        pass

    def _update_license_status(rgb):
        # Uses: format
        pass

    def _update_status_ui(self, pid, message):
        """
        
        Update status text for a given profile id (pid).
        
        """
        # Local variables: ui
        # Uses: ui, get, value, color, update, page
        pass

    def _update_tag(self, key, value):
        # Local variables: lic
        # Uses: accounts
        pass

    def PurchaseUI():
        # Uses: reset_ui, set_selected_crypto, clear_crypto_selection, view
        pass

    def PurchaseUI(self, on_crypto_click, on_apply_coupon, amount, quantity, scrapers):
        # Uses: selected_crypto_btn, ft, Image, DEFAULT_QR, qr_image, Text, Colors, GREY_500, address_label, amount_label
        pass

    def PurchaseUI(self, on_click):
        # Local variables: crypto_button, url, label, ident
        # Uses: ft, Container, Colors, TRANSPARENT, Column, ResponsiveRow, CRYPTO_OPTIONS
        pass

    def PurchaseUI(url, label, identifier):
        # Local variables: btn
        # Uses: ft, ElevatedButton, Row, Image, Text, Colors, WHITE, ButtonStyle, Padding, GREY_800
        pass

    def PurchaseUI(self):
        # Uses: selected_crypto_btn, ft, Colors, GREY_800, style, bgcolor, update
        pass

    def PurchaseUI(self):
        # Local variables: w, ex
        # Uses: DEFAULT_QR, qr_image, src, address_label, value, amount_label, expires_label, coupon_input, current, apply_btn
        pass

    def PurchaseUI(self, button):
        # Uses: clear_crypto_selection, selected_crypto_btn, ft, Colors, GREEN_800, style, bgcolor, update
        pass

    def PurchaseUI(self):
        # Uses: ft, Column, Divider, Colors, TRANSPARENT, Container, Text, FontWeight, BOLD, WHITE
        pass

    def run_bootstrap(self, page):
        """
        
        Public bootstrap entry, identical to previous behavior.
        It renders the identity screen (create/restore) and moves to main().
        
        """
        # Uses: page
        pass

    def run_main(self, page, restore):
        """
        
        Public main entry, identical to previous behavior.
        
        """
        # Uses: page, CLIENT_ID, CLIENT_PASSWORD, run_task
        pass


# =============================================================================
# STANDALONE FUNCTIONS
# =============================================================================

def XBotApp():
    # Uses: ft, Page, run_bootstrap, bool, run_main, int, dict, list, str, PurchaseUI
    pass

def _get_app():
    # Uses: XBotApp
    pass

def bootstrap(page):
    # Uses: run_bootstrap
    pass

def main(page, restore):
    # Uses: run_main
    pass


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    import flet as ft
    ft.app(target=bootstrap)
