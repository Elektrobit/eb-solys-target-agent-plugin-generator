#include <iostream>


#include "UniquePluginNamePlugin.hpp"


extern "C" void* createPluginInstance(const CMessageDispatcher* const senderHandle, const CTimestampProvider* tsProvider) {
	return new TargetAgentUniquePluginNamePlugin::CUniquePluginNamePlugin(senderHandle, tsProvider);
}

namespace TargetAgentUniquePluginNamePlugin {

using namespace TargetAgent;

CUniquePluginNamePlugin::CUniquePluginNamePlugin(const CMessageDispatcher* const senderHandle, const CTimestampProvider* tsProvider) :mMsgSenderHDL(senderHandle),mTimestampProvider(tsProvider),
		messageTypeSocketReader(
				Protocol::CommonDefinitions::MSG_TYPE_UniquePluginUpName_PLUGIN), logger(
				0) {
	logger = &(Poco::Logger::get("TargetAgent.CUniquePluginNamePlugin")); // inherits configuration from Target Agent
}

CUniquePluginNamePlugin::~CUniquePluginNamePlugin() {
}

bool CUniquePluginNamePlugin::setConfig(
		const std::map<std::string, std::string>& pluginConfiguration) {
    logger->warning("setConfig");
	return true;
}

void CUniquePluginNamePlugin::onMessageReceived(int payloadLength,
		const unsigned char* payloadBuffer) {

}

Protocol::CommonDefinitions::MessageType CUniquePluginNamePlugin::MessageType() {
	return messageTypeSocketReader;
}

void CUniquePluginNamePlugin::onConnectionEstablished() {
}

void CUniquePluginNamePlugin::onConnectionLost() {
	logger->warning(
			"Connection Lost: trigger metadata dispatch, currently none");
}

bool CUniquePluginNamePlugin::startPlugin() {
    logger->warning("startPlugin");
	return true;
}

bool CUniquePluginNamePlugin::stopPlugin() {
    logger->warning("stopPlugin");
	return true;
}

}
;
