class Credentials {
    static baseUrl = 'http://127.0.0.1:8800'
    static projectId = null;
    static apiId = null;
    static apiKey = null;
}

const container = document.getElementById('conceptuneChatbot');
Credentials.projectId = container.getAttribute('projectId');
Credentials.apiId = container.getAttribute('apiId');
Credentials.apiKey = container.getAttribute('apiKey');

class HttpClient {

    constructor() {}

    static async _base(method, path, headers, data) {
        try {
            const url = Credentials.baseUrl + path
            const response = await fetch(url, {
                method: method,
                headers: headers,
                credentials: 'include',
                body: JSON.stringify(data)
            });
            return response.json();
        } catch(e) {
            return {
                success: false
            }
        }
    }

    static async post(path, headers, data) {
        return await this._base('POST', path, headers, data);
    }

    static async get(path, headers, data) {
        return await this._base('GET', path, headers, data);
    }
}

class TokenAuthentication {
    authPath = `/customer/v1/auth/?project_id=${Credentials.projectId}`;

    constructor() {}

    async authenticate() {
        await HttpClient.get(this.authPath);
    }
}

const tokenAuth = new TokenAuthentication();
tokenAuth.authenticate();