// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SupplyChainTrace {
    
    address public owner;
    mapping(address => bool) public authorizedRegistrars;

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
    event RegistrarAdded(address indexed account);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this");
        _;
    }

    modifier onlyAuthorized() {
        require(msg.sender == owner || authorizedRegistrars[msg.sender], "Not authorized");
        _;
    }

    constructor() {
        owner = msg.sender;
        authorizedRegistrars[msg.sender] = true;
    }

    function addRegistrar(address _account) public onlyOwner {
        authorizedRegistrars[_account] = true;
        emit RegistrarAdded(_account);
    }

    function createBatch(string memory _publicId, string memory _batchType, string memory _origin) public onlyAuthorized {
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
    
    function addEvent(string memory _publicId, string memory _eventType, uint256 _timestamp) public onlyAuthorized {
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
