// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SupplyChainTrace {
    
    struct BatchInfo {
        string publicId;
        string batchType;
        string origin;
        address creator;
        uint256 createdAt;
    }
    
    struct EventInfo {
        string eventType;
        uint256 timestamp;
        address recorder;
    }
    
    mapping(string => BatchInfo) public batches;
    mapping(string => EventInfo[]) public batchEvents;
    
    event BatchCreated(string publicId, string batchType, string origin);
    event EventAdded(string publicId, string eventType, uint256 timestamp);
    
    function createBatch(string memory _publicId, string memory _batchType, string memory _origin) public {
        require(bytes(batches[_publicId].publicId).length == 0, "Batch already exists");
        
        batches[_publicId] = BatchInfo({
            publicId: _publicId,
            batchType: _batchType,
            origin: _origin,
            creator: msg.sender,
            createdAt: block.timestamp
        });
        
        emit BatchCreated(_publicId, _batchType, _origin);
    }
    
    function addEvent(string memory _publicId, string memory _eventType, uint256 _timestamp) public {
        require(bytes(batches[_publicId].publicId).length != 0, "Batch does not exist");
        
        batchEvents[_publicId].push(EventInfo({
            eventType: _eventType,
            timestamp: _timestamp,
            recorder: msg.sender
        }));
        
        emit EventAdded(_publicId, _eventType, _timestamp);
    }
    
    function getEvents(string memory _publicId) public view returns (EventInfo[] memory) {
        return batchEvents[_publicId];
    }
}
