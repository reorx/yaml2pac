var assert = require('assert');
var cidr = require('../yaml2pac/data/cidr_match.js');

var test_data = [
    // exact ip
    ['10.10.0.0', '10.10.0.0', true],
    ['10.10.0.1', '10.10.0.0', false],

    // 32
    ['10.10.0.0', '10.10.0.0/32', true],

    // 32
    ['10.10.0.0', '10.10.0.0/32', true],

    // 31
    ['10.10.0.1', '10.10.0.0/31', true],
    ['10.10.0.0', '10.10.0.1/31', true],
    ['10.10.0.2', '10.10.0.1/31', false],

    // 24
    ['10.10.0.0', '10.10.0.0/24', true],
    ['10.10.0.255', '10.10.0.0/24', true],
    ['10.10.1.255', '10.10.0.0/24', false],
    // all the same, except last number
    ['10.10.0.0', '10.10.0.1/24', true],
    ['10.10.0.255', '10.10.0.128/24', true],
    ['10.10.1.255', '10.10.0.255/24', false],

    // 16
    ['192.168.0.0', '192.168.0.0/16', true],
    ['192.168.255.255', '192.168.0.0/16', true],
    ['192.169.0.0', '192.168.0.0/16', false],
    // all the same, except last two number
    ['192.168.0.0', '192.168.1.1/16', true],
    ['192.168.255.255', '192.168.128.128/16', true],
    ['192.169.0.0', '192.168.256.256/16', false],
];

describe('cidr_match()', function () {
    test_data.forEach(function(i) {
        var ip = i[0],
            ip_cidr = i[1],
            rv = i[2];
        it('`' + ip + '` ' + (rv ? 'match' : 'dismatch') + ' to `' + ip_cidr + '`cidr range', function () {
            assert.equal(
                cidr.cidr_match(ip, ip_cidr), rv
            );
        });
    });
});
