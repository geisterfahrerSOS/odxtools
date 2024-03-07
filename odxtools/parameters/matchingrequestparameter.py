# SPDX-License-Identifier: MIT
from dataclasses import dataclass
from typing import Optional

from typing_extensions import override

from ..decodestate import DecodeState
from ..encodestate import EncodeState
from ..exceptions import EncodeError
from ..odxtypes import DataType, ParameterValue
from .parameter import Parameter, ParameterType


@dataclass
class MatchingRequestParameter(Parameter):
    request_byte_position: int
    byte_length: int

    @property
    def parameter_type(self) -> ParameterType:
        return "MATCHING-REQUEST-PARAM"

    def get_static_bit_length(self) -> Optional[int]:
        return 8 * self.byte_length

    @property
    def is_required(self) -> bool:
        return False

    @property
    def is_settable(self) -> bool:
        return False

    def get_coded_value_as_bytes(self, encode_state: EncodeState) -> bytes:
        if not encode_state.triggering_request:
            raise EncodeError(f"Parameter '{self.short_name}' is of matching request type,"
                              " but no original request has been specified.")
        return encode_state.triggering_request[self
                                               .request_byte_position:self.request_byte_position +
                                               self.byte_length]

    @override
    def _decode_positioned_from_pdu(self, decode_state: DecodeState) -> ParameterValue:
        result = decode_state.extract_atomic_value(
            bit_length=self.byte_length * 8,
            base_data_type=DataType.A_UINT32,
            is_highlow_byte_order=False)

        return result
