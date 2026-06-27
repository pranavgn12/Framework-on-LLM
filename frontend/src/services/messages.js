import api from "./api";

export async function getMessages(conversationId) {

    const response = await api.get(

        `/messages/${conversationId}`

    );

    return response.data;

}

export async function sendMessage(

    conversation_id,

    content

) {

    const response = await api.post(

        "/messages/send",

        {

            conversation_id,

            content

        }

    );

    return response.data;

}