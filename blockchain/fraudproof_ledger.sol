// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract FraudProofLedger {

    struct FraudRecord {
        bytes32 transactionHash;
        uint256 fraudScore;
        string modelVersion;
        uint256 timestamp;
    }

    FraudRecord[] public records;

    event FraudLogged(
        bytes32 transactionHash,
        uint256 fraudScore,
        string modelVersion,
        uint256 timestamp
    );

    function logFraud(
        bytes32 _transactionHash,
        uint256 _fraudScore,
        string memory _modelVersion
    ) public {
        records.push(
            FraudRecord(
                _transactionHash,
                _fraudScore,
                _modelVersion,
                block.timestamp
            )
        );

        emit FraudLogged(
            _transactionHash,
            _fraudScore,
            _modelVersion,
            block.timestamp
        );
    }

    function getRecordsCount() public view returns (uint256) {
        return records.length;
    }
}
