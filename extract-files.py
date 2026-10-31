#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'hardware/qcom-caf/sm6375-6.1',
    'hardware/qcom-caf/wlan',
    'hardware/xiaomi',
    'vendor/qcom/opensource/commonsys/display',
    'vendor/qcom/opensource/commonsys-intf/display',
    'vendor/qcom/opensource/dataservices',
]


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'vendor.qti.diaghal@1.0',
        'vendor.qti.hardware.wifidisplaysession@1.0',
        'vendor.qti.ImsRtpService-V1-ndk',
        'vendor.qti.imsrtpservice@3.0',
        'vendor.qti.imsrtpservice@3.1',
    ): lib_fixup_vendor_suffix,
}


blob_fixups: blob_fixups_user_type = {
    'system_ext/etc/vintf/manifest/vendor.qti.qesdsys.service.xml': blob_fixup()
        .regex_replace(r'(?s)^.*?(?=<manifest)', ''),
    'system/framework/WfdCommon.jar': blob_fixup()
        .apktool_patch('blob-patches/WfdCommon.patch'),
    'system_ext/lib64/libwfdservice.so': blob_fixup()
        .replace_needed('android.media.audio.common.types-V4-cpp.so', 'android.media.audio.common.types-V5-cpp.so'),
    (
        'odm/bin/hw/vendor.xiaomi.sensor.citsensorservice.aidl',
        'odm/lib64/hw/displayfeature.default.so',
        'vendor/bin/hw/vendor.qti.camera.provider-service_64',
        'vendor/bin/hw/vendor.qti.hardware.display.composer-service',
        'vendor/lib64/camx.provider-impl.so',
        'vendor/lib64/libdpps.so',
        'vendor/lib64/liblearningmodule.so',
        'vendor/lib64/libsnapdragoncolor-manager.so',
    ): blob_fixup()
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v34.so'),
    (
        'vendor/bin/qcc-vendor',
        'vendor/bin/qms',
        'vendor/bin/xtra-daemon',
        'vendor/lib64/libcne.so',
        'vendor/lib64/libqcc_sdk.so',
        'vendor/lib64/libqms_client.so',
    ): blob_fixup()
        .add_needed('libbinder_shim.so'),
    'vendor/lib64/libqcodec2_core.so': blob_fixup()
        .add_needed('libcodec2_shim.so'),
    'vendor/lib64/vendor.libdpmframework.so': blob_fixup()
        .add_needed('libbinder_shim.so')
        .add_needed('libhidlbase_shim.so'),
    'vendor/lib64/libMiVideoFilter.so': blob_fixup()
        .clear_symbol_version('AHardwareBuffer_allocate')
        .clear_symbol_version('AHardwareBuffer_describe')
        .clear_symbol_version('AHardwareBuffer_lockPlanes')
        .clear_symbol_version('AHardwareBuffer_release')
        .clear_symbol_version('AHardwareBuffer_unlock'),
    'vendor/lib64/libTrueSight.so': blob_fixup()
        .clear_symbol_version('AHardwareBuffer_allocate')
        .clear_symbol_version('AHardwareBuffer_describe')
        .clear_symbol_version('AHardwareBuffer_lock')
        .clear_symbol_version('AHardwareBuffer_lockPlanes')
        .clear_symbol_version('AHardwareBuffer_release')
        .clear_symbol_version('AHardwareBuffer_unlock'),
    'vendor/etc/seccomp_policy/c2audio.vendor.ext-arm64.policy': blob_fixup()
        .add_line_if_missing('setsockopt: 1'),
    'vendor/etc/media_codecs_blair.xml': blob_fixup()
        .regex_replace('.*media_codecs_(google_audio|google_telephony|vendor_audio|google_c2|dolby_audio).*\n', ''),
    'vendor/lib64/libcameraopt.so': blob_fixup()
        .add_needed('libprocessgroup_shim.so'),
    'vendor/etc/vintf/manifest/c2_manifest_vendor_spring.xml': blob_fixup()
        .regex_replace('.+DOLBY.+\n', ''),
    ('vendor/lib64/libqcrilNr.so', 'vendor/lib64/libril-db.so'): blob_fixup()
        .binary_regex_replace(rb'persist\.vendor\.radio\.poweron_opt', rb'persist.vendor.radio.poweron_ign'),
}  # fmt: skip

# BEGIN SPRING VERIFIED LIVE BEAUTY FIX
from extract_utils.fixups_blob import blob_fixup as _spring_beauty_fixup
_spring_beauty_key = 'vendor/lib64/camera/components/com.mi.node.tsskinbeautifier.so'
_spring_beauty_chain = blob_fixups.get(_spring_beauty_key, _spring_beauty_fixup())
blob_fixups[_spring_beauty_key] = (_spring_beauty_chain
    .sig_replace('00 20 80 52 f6 17 00 f9 ff 7f 04 a9 b2 10 00 94', '00 a6 81 52 f6 17 00 f9 ff 7f 04 a9 b2 10 00 94')
    .sig_replace('00 20 80 52 a0 10 00 94 a3 12 44 29 e1 03 18 aa', '00 a6 81 52 a0 10 00 94 a3 12 44 29 e1 03 18 aa')
)
# END SPRING VERIFIED LIVE BEAUTY FIX

# BEGIN SPRING VERIFIED REAR PORTRAIT FIX
# Permit rear Portrait processing when xiaomi.qvga.light.number is absent.
# Keep the existing decision when that metadata is present.
from extract_utils.fixups_blob import blob_fixup as _spring_portrait_fixup
_spring_portrait_key = 'vendor/lib64/com.xiaomi.plugin.mibokeh.so'
_spring_portrait_chain = blob_fixups.get(_spring_portrait_key, _spring_portrait_fixup())
blob_fixups[_spring_portrait_key] = (_spring_portrait_chain
    .sig_replace(
        'e8 03 40 f9 48 04 00 b4 89 00 00 90 29 1d 42 f9',
        'e8 03 40 f9 08 04 00 b4 89 00 00 90 29 1d 42 f9',
    )
)
# END SPRING VERIFIED REAR PORTRAIT FIX

module = ExtractUtilsModule(
    'spring',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    add_firmware_proprietary_file=True,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
